$(document).ready(function () {
    $('#dataTable').DataTable({
        scrollX: true,
    });
});
function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}