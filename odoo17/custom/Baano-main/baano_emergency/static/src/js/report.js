/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class BaanoReportDashboard extends Component {
	static template = "BaanoReports";

	setup() {
		// Inject the rpc and action services from Odoo
		this.rpc = useService("rpc");
		this.action = useService("action"); // Fix: Inject action service

		// Load counts after component has mounted
		onMounted(() => {
			setTimeout(() => {
				this._loadCounts();
			}, 0);
		});
	}

	/**
	 * Fetches the record count for each card based on its
	 * data-model and data-domain attributes, then updates
	 * the corresponding .card-count element.
	 */
	async _loadCounts() {
		if (!this.el) {
			console.warn("Component element is not available.");
			return;
		}

		// Select all elements with the .card-count class inside this component
		const countEls = this.el.querySelectorAll(".card-count");

		await Promise.all(
			Array.from(countEls).map(async (el) => {
				const model = el.dataset.model;
				const domain = JSON.parse(el.dataset.domain || "[]");
				try {
					// Call the Odoo backend to get the record count
					const count = await this.rpc.call("/web/dataset/call_kw", {
						model,
						method: "search_count",
						args: [domain],
					});
					el.textContent = count;
				} catch (error) {
					console.error(`Failed to load count for ${model}:`, error);
				}
			})
		);
	}

	/**
	 * Opens the report wizard for the given report type.
	 */
	openWizard(ev) {
		const reportType = ev.currentTarget.dataset.reportType;
		this.action.doAction("baano_emergency.action_baano_report_wizard", {
			additionalContext: { default_report_type: reportType },
		});
	}
}

// Register the action so Odoo can invoke it by XML
registry
	.category("actions")
	.add("baano_dashboard_action", BaanoReportDashboard);
