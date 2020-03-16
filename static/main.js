var tr=document.querySelectorAll('#countries tr')
var input=document.querySelector('input')
var i
var data

function myFunc(){
  data=[]
  for(i of tr){
      var tdata = i.getElementsByClassName('country')
      if (tdata[0] == undefined)
          continue
      data.push(tdata[0])
  }
  for(i=0;i<data.length;i++){
      var flag = false;
      var text = data[i].innerText.toLowerCase()
      if (text.trim().startsWith(input.value.toLowerCase()))
          flag = true
      for (s of text.split(" ")) {
          if( s.trim().startsWith(input.value.toLowerCase()))
              flag = true
      }
      if (flag)
          tr[i+1].style.display=""
      else
          tr[i+1].style.display="none"
   }
}
