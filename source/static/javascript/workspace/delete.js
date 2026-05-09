const input = document.getElementById("workspace_name");
const confirmBtn = document.getElementById("delete-confirm-btn");

function resetDeleteModal() {
    input.value = "";
    confirmBtn.disabled = true;
}

input?.addEventListener("input", () => {
    const expected = input.dataset.workspaceName.trim();
    confirmBtn.disabled = input.value.trim() !== expected;
});