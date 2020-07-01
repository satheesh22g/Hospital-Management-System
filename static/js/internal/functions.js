// function for get patient medicine histry data using ajax by passing patient ID
function getMedHist(ele,id){
    var data = {"id": id}
    $.ajax({
        type: "GET",
        url: "/api/v1/getmedhist",
        dataType: 'json',
        data: data,
        async:false,
    }).done(function(result){
      $('#med_issued').find('tbody').html('')
      if(result.query_status == 'fail'){
      }
      else{
        result.forEach(i => {
            temp = '<tr><td><div class="m_name">'+i.name+'</div></td><td><div class="m_quantity">'+i.quantity+'</div></td><td><div class="m_rate">'+i.rate+'</div></td><td><div class="m_amount">'+i.amount+'</div></td></tr>'
            $('#med_issued').find('tbody').append(temp)
        });
      }
    }).fail(function(error){
        alert('error')
    })
}

// function for get patient diagnostics histry data using ajax by passing patient ID
function getDiaHist(ele,id){
  var data = {"id": id}
  $.ajax({
      type: "GET",
      url: "/api/v1/getdiahist",
      dataType: 'json',
      data: data,
      async:false,
  }).done(function(result){
    $('#diagno_conduct').find('tbody').html('')
    if(result.query_status == 'fail'){
    }
    else{
      result.forEach(i => {
          temp = '<tr><td><div class="d_name">'+i.name+'</div></td><td><div class="d_count">'+i.count+'</div></td><td><div class="d_amount">'+i.amount+'</div></td></tr>'
          $('#diagno_conduct').find('tbody').append(temp)
      });
    }
  }).fail(function(error){
      alert('error')
  })
}

// function for get patient data using ajax by passing patient ID
function getPatientData(ele,id){
    var data = {"id": id}
    $.ajax({
        type: "GET",
        url: "/api/v1/getPatientData",
        dataType: 'json',
        data: data,
        async:false,
    }).done(function(result){
        if(result.query_status == 'fail'){
          if(!$(ele).hasClass('add_patient')){
            alert(result.message)
            $(ele).val('')
            $("input[type=textfield]").val('');
            $("input[type=date]").val('');
            $("input[type=number]").val('');
            
            if( $('#med_issued').length || $('#diagno_conduct').length ){
              if($('#med_issued').length)
                $('#med_issued').find('tbody').html('')
              else if($('#diagno_conduct').length)
                $('#diagno_conduct').find('tbody').html('')
              $('.p_name').html('')
              $('.p_age').html('')
              $('.p_doa').html('')
              $('.p_tob').html('')
              $('.p_address').html('')
            }
          }
        }
        else{
            if($(ele).hasClass('issue_med') || $(ele).hasClass('add_diagno')){
                $(ele).val(result.id)
                $(ele).closest('tr').find('.p_name').html(result.name)
                $(ele).closest('tr').find('.p_age').html(result.age)
                $(ele).closest('tr').find('.p_doa').html(result.DateofAdm)
                $(ele).closest('tr').find('.p_tob').html(result.TypeofBed)
                $(ele).closest('tr').find('.p_address').html(result.address+','+result.city+','+result.state)
                
                if($(ele).hasClass('issue_med')){
                  getMedHist(ele,result.id)
                }
                else if($(ele).hasClass('add_diagno')){
                  getDiaHist(ele,result.id)
                }
            }
            else if($(ele).hasClass('add_patient')){
              alert('Paitent Id already present, Please change your input')
              $(ele).val('')
            }
            else{
                $(ele).val(result.id)
                $(ele).closest('tbody').find('input[name=name]').val(result.name)
                $(ele).closest('tbody').find('input[name=age]').val(result.age)
                $(ele).closest('tbody').find('input[name=doa]').val(result.DateofAdm)
                $(ele).closest('tbody').find('select[name=typeofbed]').val(result.TypeofBed)
                $(ele).closest('tbody').find('input[name=address]').val(result.address)
                $(ele).closest('tbody').find('input[name=state]').val(result.state)
                $(ele).closest('tbody').find('input[name=city]').val(result.city)
            }
        }
        
    }).fail(function(error){
        alert('error')
    })
}

// function for get Medicine data using ajax by passing medicine Name
function getMedicine(ele,name){
    var data = {"name": name}
    $.ajax({
        type: "GET",
        url: "/api/v1/getmedicine",
        dataType: 'json',
        data: data,
        async:false,
    }).done(function(result){
      if(result.query_status == 'fail'){
        alert(result.message)
        $(ele).val('')
      }
      else{
        $(ele).val(result.name)
        $(ele).closest('tr').find('input[name=rate]').val(result.rate)
        $(ele).closest('tr').find('input[name=rate]').attr("disabled",false)
        $(ele).closest('tr').find('input[name=quantity]').attr("data-max",result.quantity)
        $(ele).closest('tr').find('input[name=quantity]').attr("disabled",false)
      }
    }).fail(function(error){
        alert('error')
    })
}

// function for get Diagnostics data using ajax by passing medicine Name
function getDiagnostic(ele,name){
  var data = {"name": name}
  $.ajax({
      type: "GET",
      url: "/api/v1/getdiagnostic",
      dataType: 'json',
      data: data,
      async:false,
  }).done(function(result){
    if(result.query_status == 'fail'){
      alert(result.message)
      $(ele).val('')
    }
    else{
      $(ele).val(result.name)
      $(ele).closest('tr').find('input[name=amount]').val(result.charge)
      $(ele).closest('tr').find('input[name=amount]').attr("disabled",false)
    }
  }).fail(function(error){
      alert('error')
  })
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