$(document).ready(function() {

    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000); // <-- time in milliseconds

    $('#showPass').click(function(){
        var x = $("#passwordInput")[0]
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    });

    $('.reset_btn').click(function(event){
        event.preventDefault();
        $("#ssn_id")[0].value = "";
        $("#name")[0].value = "";
        $("#doa")[0].value = '';
        $("#address")[0].value = "";
        $("#age")[0].value = "";
        $("#state")[0].value = "";
        $("#city")[0].value = "";
    });

    $('#ssn_id, #age, #amount').keypress(function(event){
        if(event.which = 8 && isNaN(String.fromCharCode(event.which))){
            event.preventDefault(); //stop character from entering input
        }
    })

    $('#ssn_id, #age, #amount').change(function (event) {
        event.preventDefault()
        test = this.parentNode.children.item(1)
        if(isNaN(parseInt(event.target.value))){
            test.innerHTML='Only Digits allowed *'
            test.style.display='block'
            event.target.value=''
        }
        else{
            test.style.display='none'
            target = event.target
            if(target.id == "ssn_id" && target.value.length != 9){
                test.innerHTML='Required 9 digits *'
                test.style.display='block'
            }
        }
    });

    $('#name, #state, #city').keypress(function(event){
        if(!((event.charCode > 64 && event.charCode < 91) || (event.charCode > 96 && event.charCode < 123) || event.charCode==32)){
            event.preventDefault(); //stop character from entering input
        }
    })

    $('#view_cust').validate({
        rules: {
            cust_id: {
                required: '#cust_ssn_id:blank'
            },
            cust_ssn_id: {
                required: '#cust_id:blank'
            }
          }
    })

    $('#view_acc').validate({
        rules: {
            cust_id: {
                required: '#acc_id:blank'
            },
            acc_id: {
                required: '#cust_id:blank'
            }
          }
    })

    $('select.sel_type').change(function () {
        if (this.value == 'current')
            $('select.sel_type').not(this).val('savings');
        if (this.value == 'savings')
            $('select.sel_type').not(this).val('current');
    });

    $('#edit_patient #ssn_id').change(function (event) {
        event.preventDefault()
        id = event.target.value
        if(!isNaN(parseInt(event.target.value)) && id.length==9){
            result = getPatientData(id)
            if(result['query_status']=='fail'){
                alert('Invaild Patient ID, Please check your input')
                event.target.value = ''
            }
            else{
                $('#edit_patient input[name=ssn_id]')[0].value = result.id
                $('#edit_patient input[name=name]')[0].value = result.name
                $('#edit_patient input[name=age]')[0].value = result.age
                $('#edit_patient input[name=doa]')[0].value = result.DateofAdm
                $('#edit_patient select[name=typeofbed]')[0].value = result.TypeofBed
                $('#edit_patient input[name=address]')[0].value = result.address
                $('#edit_patient input[name=state]')[0].value = result.state
                $('#edit_patient input[name=city]')[0].value = result.city
            }
        }
    });
    $('#add_patient #ssn_id').change(function (event) {
        event.preventDefault()
        id = event.target.value
        if(!isNaN(parseInt(event.target.value)) && id.length==9){
            result = getPatientData(id)
            if(result['query_status']!='fail'){
                alert('Patient ID already present, Please change your input')
                event.target.value = ''
            }
        }
    });

    $('.refresh').click(function(event){
        event.preventDefault()
        target = event.target
        cust_id = parseInt(target.dataset.cust_id)
        var data = {"cust_id": cust_id}
        $.ajax({
            type: "POST",
            url: "/api/v1/customerlog",
            dataType: 'json',
            data: JSON.stringify(data),
            contentType:"application/json; charset=UTF-8"
        }).done(function(result){
            console.log(result)
            parrent_ele = target.parentElement.parentElement
            parrent_ele.children[2].innerHTML = result.message
            parrent_ele.children[3].innerHTML = result.date
        }).fail(function(error){
            console.log(error)
        })
    })
});

function getPatientData(id){
    var result_data = {}
    var data = {"id": id}
    $.ajax({
        type: "GET",
        url: "/api/v1/getPatientData",
        dataType: 'json',
        data: data,
        async:false,
    }).done(function(result){
        result_data = result
    }).fail(function(error){
        result_data = error
    })
    return result_data
}

function getPagination(table) {

    $('#maxRows').on('change', function(e) {
      $('.pagination').html(''); // reset pagination
      var trnum = 0; // reset tr counter
      var maxRows = parseInt($(this).val()); // get Max Rows from select option
      var totalRows = $(table + ' tbody tr').length; // numbers of rows
      $(table + ' tr:gt(0)').each(function() { // each TR in  table and not the header
        trnum++; // Start Counter
        if (trnum > maxRows) { // if tr number gt maxRows
  
          $(this).hide(); // fade it out
        }
        if (trnum <= maxRows) {
          $(this).show();
        } // else fade in Important in case if it ..
      }); //  was fade out to fade it in
      if (totalRows > maxRows) { // if tr total rows gt max rows option
        var pagenum = Math.ceil(totalRows / maxRows); // ceil total(rows/maxrows) to get ..
        //	numbers of pages
        for (var i = 1; i <= pagenum;) { // for each page append pagination li
          $('.pagination').append('<li class"wp" data-page="' + i + '">\
  <span>' + i++ + '<span class="sr-only">(current)</span></span>\
  </li>').show();
        } // end for i
      } // end if row count > max rows
      $('.pagination li:first-child').addClass('active'); // add active class to the first li
      $('.pagination li').on('click', function() { // on click each page
        var pageNum = $(this).attr('data-page'); // get it's number
        var trIndex = 0; // reset tr counter
        $('.pagination li').removeClass('active'); // remove active class from all li
        $(this).addClass('active'); // add active class to the clicked
        $(table + ' tr:gt(0)').each(function() { // each tr in table not the header
          trIndex++; // tr index counter
          // if tr index gt maxRows*pageNum or lt maxRows*pageNum-maxRows fade if out
          if (trIndex > (maxRows * pageNum) || trIndex <= ((maxRows * pageNum) - maxRows)) {
            $(this).hide();
          } else {
            $(this).show();
          } //else fade in
        }); // end of for each tr in table
      }); // end of on click pagination list
  
  
    });
}