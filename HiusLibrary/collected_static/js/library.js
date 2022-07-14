
    function openForm() {
        document.getElementById("myForm").style.display = "block";
    }

    function closeForm() {
        document.getElementById("myForm").style.display = "none";
    }

    var myModal = document.getElementById('myModal')
    var myInput = document.getElementById('myInput')

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus()
    })

   $(document).ready(function () {
    $('.banbutton').click(function (e) {
        e.preventDefault();
        var catid;
        catid = $(this).attr("ban-data");
        var NAME = document.getElementById("ban" + catid)
        var isBanned = $(this).attr("is-banned");
        $.ajax(
            {
                type: "GET",
                url: "{% url 'banUser' %}",
                data: {
                    catid: catid,
                },
                success: function (data) {
                    $('#bannedBy' + catid).load(data)
                }
            });

    })
       })

    $(document).ready(function () {
        $(".banbutton").click(function () {
            var catid;
            catid = $(this).attr("ban-data");
            var isBanned = $(this).attr("is-banned");
            if (isBanned === 'FALSE') {
                $("#ban" + catid).removeClass('btn-warning').addClass('btn-danger').html("<i class='fas fa-lock'></i>");
                $("#ban" + catid).attr("is-banned", "TRUE");
                $('#extend' + catid).hide()
                $('#wev').show()
                $('#bannedBy' + catid).show()
            } else if (isBanned === 'TRUE') {
                $("#ban" + catid).removeClass('btn-danger').addClass('btn-warning').html("<i class='fas fa-unlock'></i>");
                $("#ban" + catid).attr("is-banned", "FALSE");
                $('#extend' + catid).show();
                $('#wev').hide()
                $('#bannedBy' + catid).hide()
            }
        });
    });

    $(document).ready(function () {
        $(".banbutton").click(function (e) {
            var thisOne;
            thisOne = $(this).attr("extend");

            function RefreshTable() {
                $('#dataTable').load("{% url 'userIndex' %} #userRow");
            }

            $('#extend' + thisOne).on("click", RefreshTable);
        })
    });