/** @odoo-module **/

function toggleAffiliation() {
    const select = document.querySelector("#affiliation_option");
    if (!select) return;
    document.querySelector(".casa-affiliation-existing")?.classList.toggle("d-none", select.value !== "existing");
    document.querySelector(".casa-affiliation-other")?.classList.toggle("d-none", select.value !== "other");
}

function toggleBranches() {
    const form = document.querySelector(".casa-branches-form");
    if (!form) return;
    const later = form.querySelector("#provide_branches_later");
    const blocks = form.querySelector("#branch_blocks");
    blocks?.classList.toggle("d-none", Boolean(later?.checked));
    blocks?.querySelectorAll("input, select").forEach((field) => {
        if (field.dataset.originalRequired === undefined) {
            field.dataset.originalRequired = field.required ? "1" : "0";
        }
        field.required = !later?.checked && field.dataset.originalRequired === "1";
    });
}

function bindCopyButton(button, branchForm) {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", () => {
        const block = button.closest(".casa-branch-block");
        const field = (suffix) => block?.querySelector(`[name$='_${suffix}']`);
        field("street").value = branchForm.dataset.headStreet || "";
        field("street2").value = branchForm.dataset.headStreet2 || "";
        field("city").value = branchForm.dataset.headCity || "";
        field("state_id").value = branchForm.dataset.headState || "";
        field("zip").value = branchForm.dataset.headZip || "";
    });
}

function resizeBranchBlocks(branchForm) {
    const container = branchForm.querySelector("#branch_blocks");
    const count = Math.max(1, Math.min(100, Number(branchForm.querySelector("#branch_count")?.value || 1)));
    let blocks = [...container.querySelectorAll(".casa-branch-block")];
    const template = blocks[0];
    while (blocks.length < count) {
        const index = blocks.length;
        const block = template.cloneNode(true);
        block.querySelector("h2 span").textContent = String(index + 1);
        block.querySelectorAll("input, select").forEach((field) => {
            field.name = field.name.replace(/branch_\d+_/, `branch_${index}_`);
            if (field.tagName === "SELECT") field.selectedIndex = 0;
            else field.value = "";
        });
        const copyButton = block.querySelector(".casa-copy-head-office");
        delete copyButton.dataset.bound;
        bindCopyButton(copyButton, branchForm);
        container.appendChild(block);
        blocks.push(block);
    }
    while (blocks.length > count) blocks.pop().remove();
    toggleBranches();
}

document.addEventListener("DOMContentLoaded", () => {
    const affiliation = document.querySelector("#affiliation_option");
    affiliation?.addEventListener("change", toggleAffiliation);
    toggleAffiliation();

    const branchForm = document.querySelector(".casa-branches-form");
    branchForm?.querySelector("#provide_branches_later")?.addEventListener("change", toggleBranches);
    branchForm?.querySelector("#branch_count")?.addEventListener("change", () => resizeBranchBlocks(branchForm));
    branchForm?.querySelectorAll(".casa-copy-head-office").forEach((button) => bindCopyButton(button, branchForm));
    toggleBranches();
});
