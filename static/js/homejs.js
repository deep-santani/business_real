var i=0;
let json_data;
function addRow(){
    $(document).ready(function(){
        $('#dataTable > tbody ').append('<tr><td>'+(i+1)+'</td><td><input type="text" size="28" name="iname"  id="iname" oninput="JsonData()"  list="items" /></td><td><input type="text" name="iquantity" onfocus="dv(this)" size="3" id="iquantity" value="0" oninput="mul()" /></td><td><input type="text" value="0" name="iprice"  size="6" id="iprice" onfocus="dv(this)" oninput="mul()"  /></td><td><input type="text" size="3" value="0" name="igst" id="igst" onfocus="dv(this)" oninput="mul()"/></td><td><input type="text" name="itotal" size="10" id="result" value="0" onfocus="dv(this)"/></td></tr>');
        i++;
    });
    calculateColumn()
    
}

function delrow(){
    if(i!=0){
        document.getElementById('dataTable').deleteRow(i);
        i--;
    }
    calculateColumn()
}

function dv(x){
    if(x.value="0"){
        x.value="";
    }
}

function mul(){
    $('document').ready(function(){
        $('#dataTable tr').each(function() {
            var iquantity=parseFloat($(this).find("td:eq(2) input[type='text']").val());
            var iprice=parseFloat($(this).find("td:eq(3) input[type='text']").val());
            var igst=parseFloat($(this).find("td:eq(4) input[type='text']").val());
            $(this).find("td:eq(5) input[type='text']").val(Math.ceil(iquantity*(iprice+igst)));
        });
    });
    
}



function calculateColumn() {
    var total = 0;
    $('table tr').each(function() {
        var value=parseFloat($(this).find("td:eq(5) input[name='itotal']").val());
        if (!isNaN(value)) {
            total += value;
        }
    });
    
    $('#tot').val(Math.ceil(total));
}


function dis1(){
    document.getElementById('discount_block').style.display="block";
    document.getElementById('discount_btn').style.display="none";
}

function dis2(){
    document.getElementById('discount_btn').style.display="block";
    document.getElementById('discount_block').style.display="none";
}

function balance(){
    
    var total=document.getElementById('tot').value;
    var discount=document.getElementById('discount').value;
    var paid=total-discount;
    document.getElementById('paid').value=Math.ceil(paid);
}


function ph_check(){
    var phno=document.getElementById('phno').value;
    if(phno.length==10){
        document.getElementById('form1').submit();
    }
}

function payment(){
    var mode=document.getElementById('payment_mode');
    var block=document.getElementById('payment_mode_description');
    if(mode.value=="Cash"){
        block.innerHTML="<div id='div8'><div><label> Payment Details</label><textarea rows='4' cols='15' name='payment_details' ></textarea></div>&emsp;<div><label> Remarks :-</label><textarea rows='4' cols='30' name='remark' ></textarea></div></div>"
    }
    else if(mode.value=="UPI"){
        block.innerHTML="<div id='div9'><div><label>Payment Gateway Name :&emsp;</label><select name='payment_gateway' id='payment_gateway'><option value=''>Select</option><option value='GooglePay'>Google Pay</option><option value='Phonepe'>PhonePe</option><option value='Paytm'>Paytm</option>"+
        "<option value='Postpe'>PostPe</option><option value='Others'>Others</option></select></div><div><label>Transaction No.:&emsp;</label><input type='text' name='payment_details'></div><div><label>Remarks :&ensp;</label><textarea rows='2' cols='30' name='remark' ></textarea></div></div>" 
    }
    else if(mode.value=="PayLater"){
        block.innerHTML="<div id='div10'><div><label>Amount Paid :&nbsp;</label>&#8377;&nbsp;<input type='text' name='pay_later_paid' id='pay_later_paid' oninput='pay_later()'></div><div><label>Balance :&emsp;</label>&#8377; &nbsp;<input type='text' name='pay_later_balance' id='pay_later_balance'></div><div><label>Remarks :&ensp;</label><textarea rows='3' cols='30' name='remark' ></textarea></div></div>"
    }
    else if(mode.value=="Other"){
        mode.style.display="none";
        block.innerHTML="<div id='div8'><div><label> Payment Details</label><textarea rows='4' cols='15' name='payment_details' ></textarea></div>&emsp;<div><label> Remarks :-</label><textarea rows='4' cols='30' name='remark' ></textarea></div></div>";
        var input=document.createElement('input');
        input.name="payment_mode";
        var close=document.createElement('input');
        close.type="button";
        close.className="btn-close";
        close.id="others_close";
        close.onclick=function(){
            mode.style.display="inline-block";
            block.innerHTML="";
            close.style.display="none";
            input.style.display="none";
            mode.value="";
        }
        mode.parentElement.insertBefore(input,mode);
        mode.parentElement.insertBefore(close,mode);   
    }
    else{
        block.innerHTML="";
    }
}

function pay_later(){
    document.getElementById('pay_later_balance').value=(document.getElementById('paid').value)-(document.getElementById('pay_later_paid').value);    
}

function refreshTime() {
  const date=document.getElementById('date');
  const time=document.getElementById('time');
  var current=new Date();
  var day=current.getDay();
  switch(day){
    case 0:
        day="Sunday";
        break;
    case 1:
        day="Monday";
        break;
    case 2:
        day="Tuesday";
        break;
    case 3:
        day="Wednesday";
        break;
    case 4:
        day="Thursday";
        break;
    case 5:
        day="Friday";
        break;
    case 6:
        day="Saturday";
        break;
    default:
        day="None";
  }
  date.textContent=current.getDate()+"/"+(current.getMonth()+1)+"/"+current.getFullYear()+" , "+day;
  time.textContent=current.getHours()+":"+current.getMinutes()+":"+current.getSeconds();
}
  setInterval(refreshTime, 1000);

$('document').ready(function(){
    $('#print').click(function(){
        window.print();
    });
});

function print(){
    document.getElementById('form1').submit();
}

function loadJSON() {
    fetch('http://127.0.0.1:8000/json/items/')
    .then(result => result.json())
    .then((output) => {
        json_data=output;
        datalist()
    }).catch(err => console.error(err));  
}
function datalist(){
    var list="";
    for(var j=0;j<json_data.length;j++){
        list+="<option value='"+json_data[j]['fields']['iname']+"'/>"
    }
    document.getElementById('items').innerHTML=list;
}


function JsonData(){
    
   
    $('document').ready(function(){
        $('#dataTable tr').each(function() {
            var iname=$(this).find("td:eq(1) input[type='text']").val();
            if(typeof(iname)!='undefined'){
                for(var a=0;a<json_data.length;a++){
                    if(json_data[a]['fields']['iname']==iname){
                        $(this).find("td:eq(3) input[type='text']").val(json_data[a]['fields']['iprice']);
                        $(this).find("td:eq(4) input[type='text']").val(json_data[a]['fields']['igst']); 
                    }
                }
            }
            else{
                $(this).find("td:eq(3) input[type='text']").val('');
                $(this).find("td:eq(4) input[type='text']").val('');

            }
        });
    })
}


