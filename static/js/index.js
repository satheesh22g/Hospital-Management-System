// keypress events to prevent entering Alphabets and special char
$(document).on('keypress','input[name=ssn_id], input[name=age], input[name=amount], input[name=quantity]',function(event){
    test = this.parentNode.children.item(1)
    if(event.which = 8 && isNaN(String.fromCharCode(event.which))){
        event.preventDefault(); //stop character from entering input
        test.innerHTML='Only Digits allowed *'
        test.style.display='block'
    }
    else{
        test.style.display='none'
    }
});

// change events to check entered input is not aplphabets and special char
$(document).on('change','input[name=ssn_id], input[name=age], input[name=amount], input[name=quantity]',function (event) {
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

// keypress events to prevent entering numbers and special char
$(document).on('keypress', 'input[name=state], input[name=city], input[name=name]', function(){
    test = this.parentNode.children.item(1)
    if(!((event.charCode > 64 && event.charCode < 91) || (event.charCode > 96 && event.charCode < 123) || event.charCode==32 || event.charCode==13)){
        event.preventDefault(); //stop Number from entering input
        test.innerHTML='Only Alphabets and Space allowed *'
        test.style.display='block'
    }
    else{
        test.style.display='none'
    }
});

// change events to check entered input is not numbers and special char
$(document).on('change', 'input[name=state], input[name=city], input[name=name]', function(){
    event.preventDefault()
    test = this.parentNode.children.item(1)
    if(!isNaN(event.target.value)){
        test.innerHTML='Only Alphabets and Space allowed *'
        test.style.display='block'
        event.target.value=''
    }
    else{
        test.style.display='none'
    }
});

// on change of medicine name fetch medicine data
$(document).on('change','#issue_med input[name=name]',function (event) {
    event.preventDefault()
    name = event.target.value.trim().toLowerCase()
    if(isNaN(name) && name.length>=2){
        result = getMedicine(name)
        if(result['query_status']=='fail'){
            alert('Medicine not found!, Please check your input')
            $(this).val(name)
        }
        else{
            $(this).val(result.name)
            $(this).closest('tr').find('input[name=rate]').val(result.rate)
            $(this).closest('tr').find('input[name=quantity]').attr("data-max",result.quantity)
            $(this).closest('tr').find('input[name=quantity]').attr("disabled",false)
        }
    }
});

// on change of quantity calculate total price
$(document).on('change','#issue_med input[name=quantity]',function (event) {
    event.preventDefault()
    max = parseInt(event.target.dataset.max)
    if(!isNaN(event.target.value)){
        quantity = parseInt(event.target.value)
        if(quantity >= max){
            alert('Medicine quantity not available!, Please change quantity.\nTotal available quantity = '+max)
        }
        else{
            rate = $('input[name=rate]').val()
            $(this).closest('tr').find('input[name=amount]').val((quantity * parseInt(rate)))
        }
    }
});

$(document).on('keypress','#issue_med input',function(event){
    if(event.charCode == 13 && event.target.name=='quantity'){
        event.preventDefault()
    }
})

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

    $('input[type=button].issue_med').click(function(event){
        event.preventDefault()
        $('#issue_med').css('display','block')
    })

    $('.reset_btn').click(function(event){
        event.preventDefault();
        $("input").val('');
    });

    $('#issue_med .add_row').click(function(event){
        event.preventDefault()
        temp = '<tr><td><div><input class="form-control" name="name" type="textfield" placeholder="Medicine Name" required minlength="2" maxlength="50"><span class="error_msg" style="position: inherit;"></span></div></td><td><div><input class="form-control" name="quantity" type="textfield" placeholder="Quantity" required min="1" minlength="1" maxlength="3"><span class="error_msg" style="position: inherit;"></span></div></td><td><input class="form-control" name="rate" type="textfield" required disabled></td><td><input class="form-control" name="amount" type="textfield" required disabled></td></tr>'
        $('#issue_med tbody').append(temp)
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

    $('#edit_patient input[name=ssn_id]').change(function (event) {
        event.preventDefault()
        id = event.target.value
        if(!isNaN(parseInt(event.target.value)) && id.length==9){
            result = getPatientData(id)
            if(result['query_status']=='fail'){
                alert('Patient ID not found!, Please check your input')
                event.target.value = ''
            }
            else{
                $(this).val(result.id)
                $(this).closest('tr').find('input[name=ssn_id]').val(result.name)
                $(this).closest('tr').find('input[name=age]').val(result.age)
                $(this).closest('tr').find('input[name=doa]').val(result.DateofAdm)
                $(this).closest('tr').find('select[name=typeofbed]').val(result.TypeofBed)
                $(this).closest('tr').find('input[name=address]').val(result.address)
                $(this).closest('tr').find('input[name=state]').val(result.state)
                $(this).closest('tr').find('input[name=city]').val(result.city)
            }
        }
    });

    $('input[name=ssn_id].issue_med').change(function (event) {
        event.preventDefault()
        id = event.target.value
        if(!isNaN(parseInt(event.target.value)) && id.length==9){
            result = getPatientData(id)
            if(result['query_status']=='fail'){
                alert('Patient ID not found!, Please check your input')
                event.target.value = ''
            }
            else{
                $(this).val(result.id)
                $(this).closest('tr').find('.p_name').html(result.name)
                $(this).closest('tr').find('.p_age').html(result.age)
                $(this).closest('tr').find('.p_doa').html(result.DateofAdm)
                $(this).closest('tr').find('.p_tob').html(result.TypeofBed)
                $(this).closest('tr').find('.p_address').html(result.address+','+result.city+','+result.state)
            }
        }
    });

    $('#add_patient input[name=ssn_id]').change(function (event) {
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

// function for get patient data using ajax by passing patient ID
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

// function for get Medicine data using ajax by passing medicine Name
function getMedicine(name){
    var result_data = {}
    var data = {"name": name}
    $.ajax({
        type: "GET",
        url: "/api/v1/getmedicine",
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

// function for get Pagination on the page where we have multiple row table data
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