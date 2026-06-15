from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Flag to lock the partner once selected
    is_your_partner = fields.Boolean(string="Is Your Partner")

    def _recompute_payment_terms_lines(self):
        """
        Override core Odoo method responsible for generating receivable/payable lines
        based on payment terms.

        Customizations:
        - Skip modification for customer refunds
        - Inject Macadams levy logic (7.5%)
        """

        
        if self.move_type in ['out_refund']:
            return super()._recompute_payment_terms_lines()

        self.ensure_one()

        # Ensure correct company context
        self = self.with_company(self.company_id)

        # Detect draft mode (important for deciding create vs new)
        in_draft_mode = self != self._origin

        # Current date (used for fallback maturity dates)
        today = fields.Date.context_today(self)

        # Ensure journal company consistency
        self = self.with_company(self.journal_id.company_id)

        # Separate receivable/payable lines from other lines
        existing_terms_lines = self.line_ids.filtered(
            lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')
        )

        others_lines = self.line_ids.filtered(
            lambda line: line.account_id.account_type not in ('asset_receivable', 'liability_payable')
        )

        # Company currency
        company_currency = (self.company_id or self.env.company).currency_id

        # Compute totals excluding receivable/payable lines
        total_balance = sum(others_lines.mapped(lambda l: company_currency.round(l.balance)))
        total_amount_currency = sum(others_lines.mapped('amount_currency'))

        # If no invoice lines exist, remove payment term lines
        if not others_lines:
            self.line_ids -= existing_terms_lines
            return

        # Compute payment term breakdown
        computation_date = self._get_payment_terms_computation_date()
        account = self._get_payment_terms_account(existing_terms_lines)

        to_compute = self._compute_payment_terms(
            computation_date,
            total_balance,
            total_amount_currency
        )

        # Create/update payment term lines
        new_terms_lines = self._compute_diff_payment_terms_lines(
            existing_terms_lines,
            account,
            to_compute
        )

        # Remove obsolete lines
        self.line_ids -= existing_terms_lines - new_terms_lines

        # ============================================================
        #  MACADAMS LEVY UPDATE (post-processing)
        # ============================================================

        new_account = self.env['account.account'].search([
            ('name', '=', 'Macadams Levy Clearing account'),
            ('code', '=', '860200')
        ], limit=1)

        # Find levy line if already created
        filtered_line_data = self.line_ids.filtered(lambda x: x.account_id == new_account)

        # Update levy line amount if partner matches
        if filtered_line_data and self.partner_id.name == 'Macadams Int (Pty) Ltd - JHB':
            cost = self.env.company.currency_id.round((self.amount_untaxed * 7.5) / 100)

            for rec in filtered_line_data:
                rec.update({
                    'name': self.payment_reference or '',
                    'debit': cost,
                    'amount_currency': cost
                })

        # Safety: remove all lines if no invoice lines
        if not self.invoice_line_ids:
            self.line_ids = [(5, 0, 0)]

        # Update due date & reference
        if new_terms_lines:
            self.payment_reference = new_terms_lines[-1].name or ''
            self.invoice_date_due = new_terms_lines[-1].date_maturity

    def _get_payment_terms_computation_date(self):
        """
        Determine which date should be used to compute payment terms.

        Priority:
        1. invoice_date
        2. invoice_date_due
        3. today
        """

        today = fields.Date.context_today(self)

        if self.invoice_payment_term_id:
            return self.invoice_date or today
        else:
            return self.invoice_date_due or self.invoice_date or today

    def _get_payment_terms_account(self, payment_terms_lines):
        """
        Determine receivable/payable account.

        Priority:
        1. Existing payment term lines
        2. Partner property account
        3. Fallback account search
        """

        if payment_terms_lines:
            return payment_terms_lines[0].account_id

        elif self.partner_id:
            if self.is_sale_document(include_receipts=True):
                return self.partner_id.property_account_receivable_id
            else:
                return self.partner_id.property_account_payable_id

        else:
            domain = [
                ('company_id', '=', self.company_id.id),
                ('account_type', '=', 'asset_receivable'
                 if self.move_type in ('out_invoice', 'out_refund', 'out_receipt')
                 else 'liability_payable'),
            ]
            return self.env['account.account'].search(domain, limit=1)

    def _compute_payment_terms(self, date, total_balance, total_amount_currency):
        """
        Compute how invoice amount is split across payment terms.

        Returns:
            List of tuples:
            (balance_company_currency, amount_currency, due_date)
        """

        if self.invoice_payment_term_id:

            # Compute in company currency
            to_compute = self.invoice_payment_term_id.compute(
                total_balance,
                date_ref=date,
                currency=self.company_id.currency_id
            )

            # Single currency case
            if self.currency_id == self.company_id.currency_id:
                return [(b[0], b[1], b[1]) for b in to_compute]

            # Multi-currency case
            else:
                to_compute_currency = self.invoice_payment_term_id.compute(
                    total_amount_currency,
                    date_ref=date,
                    currency=self.currency_id
                )
                return [(b[0], b[1], ac[1]) for b, ac in zip(to_compute, to_compute_currency)]

        # No payment term → full amount due immediately
        else:
            return [(date, total_balance, total_amount_currency)]

    def _compute_diff_payment_terms_lines(self, existing_terms_lines, account, to_compute):
        """
        Core method:
        - Updates existing receivable/payable lines
        - Creates new ones if needed
        - Injects Macadams levy logic
        """

        today = fields.Date.context_today(self)
        in_draft_mode = self != self._origin

        # Sort lines by maturity date
        existing_terms_lines = existing_terms_lines.sorted(
            lambda line: line.date_maturity or today
        )

        existing_terms_lines_index = 0
        new_terms_lines = self.env['account.move.line']

        # Levy account
        new_account = self.env['account.account'].search([
            ('name', '=', 'Macadams Levy Clearing account'),
            ('code', '=', '860200')
        ], limit=1)

        for date_maturity, balance, amount_currency in to_compute:

            currency = self.journal_id.company_id.currency_id

            # Skip zero lines
            if currency and currency.is_zero(balance) and len(to_compute) > 1:
                continue

            filtered_line_data = self.line_ids.filtered(
                lambda x: x.account_id == new_account
            )

            # ========================================================
            #  UPDATE EXISTING LINE
            # ========================================================
            if existing_terms_lines_index < len(existing_terms_lines):

                candidate = existing_terms_lines[existing_terms_lines_index]
                existing_terms_lines_index += 1

                # --- Macadams special logic ---
                if self.partner_id.name == 'Macadams Int (Pty) Ltd - JHB':
                    if candidate.account_id.account_type == 'asset_receivable':

                        # Compute levy (7.5%)
                        cost = self.env.company.currency_id.round(
                            (self.amount_untaxed * 7.5) / 100
                        )

                        # Adjust receivable
                        new_balance = self.amount_total - cost

                        candidate.update({
                            'date_maturity': date_maturity,
                            'debit': new_balance,
                            'amount_currency': new_balance,
                        })

                # Create levy line if not present
                if not filtered_line_data and self.partner_id.name == 'Macadams Int (Pty) Ltd - JHB':

                    cost = self.env.company.currency_id.round(
                        (self.amount_untaxed * 7.5) / 100
                    )

                    create_method = (
                        self.env['account.move.line'].new
                        if in_draft_mode else
                        self.env['account.move.line'].create
                    )

                    new_line = create_method({
                        'name': self.payment_reference or '',
                        'debit': cost,
                        'credit': 0.0,
                        'quantity': 1.0,
                        'amount_currency': cost,
                        'date_maturity': date_maturity,
                        'move_id': self.id,
                        'currency_id': self.currency_id.id,
                        'account_id': new_account.id,
                        'partner_id': self.commercial_partner_id.id,
                        'exclude_from_invoice_tab': True,
                    })

                    new_terms_lines += new_line

                # Standard logic for other partners
                if self.partner_id.name != 'Macadams Int (Pty) Ltd - JHB':
                    candidate.update({
                        'date_maturity': date_maturity,
                        'amount_currency': -amount_currency,
                        'debit': balance < 0.0 and -balance or 0.0,
                        'credit': balance > 0.0 and balance or 0.0,
                    })

            # ========================================================
            #  CREATE NEW LINE
            # ========================================================
            else:
                create_method = (
                    self.env['account.move.line'].new
                    if in_draft_mode else
                    self.env['account.move.line'].create
                )

                candidate = create_method({
                    'name': self.payment_reference or '',
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': balance > 0.0 and balance or 0.0,
                    'quantity': 1.0,
                    'amount_currency': -amount_currency,
                    'date_maturity': date_maturity,
                    'move_id': self.id,
                    'currency_id': self.currency_id.id,
                    'account_id': account.id,
                    'partner_id': self.commercial_partner_id.id,
                    'exclude_from_invoice_tab': True,
                })

            new_terms_lines += candidate

            # Trigger onchange recomputation in draft mode
            if in_draft_mode:
                candidate.update(
                    candidate._get_fields_onchange_balance(force_computation=True)
                )

        return new_terms_lines

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """
        Prevent changing partner once locked.
        """

        res = super()._onchange_partner_id()

        if self.partner_id.name == 'Macadams Int (Pty) Ltd - JHB':
            self.is_your_partner = True

        if self.is_your_partner and self.partner_id.name != 'Macadams Int (Pty) Ltd - JHB':
            raise ValidationError(_('You Can not change your partner'))

        return res