let json_data;
let items_data;
function loadJSON() {
    fetch('http://127.0.0.1:8000/json/customers/')
    .then(result => result.json())
    .then((output) => {
        json_data=output;
        customers()
    }).catch(err => console.error(err));  

    fetch('http://127.0.0.1:8000/json/items/')
    .then(result => result.json())
    .then((output) => {
        items_data=output;
        datalist()
    }).catch(err => console.error(err));  
}

function datalist(){
    var list="";
    for(var j=0;j<items_data.length;j++){
        list+="<option value='"+items_data[j]['fields']['iname']+"'/>"
    }
    document.getElementById('items').innerHTML=list;
}

function customers(){
    var list="";
    for(var j=0;j<json_data.length;j++){
        list+="<option value='"+json_data[j]['fields']['name']+"'>"+json_data[j]['fields']['name']+"</option>"
    }
    document.getElementById('cname').innerHTML+=list;
}

function customers_onchange(){
    document.getElementById("cname_form").submit()
}

function convertion(){
   
}