function check () {
    let userid = document.getElementById("userid").value
    let userage = document.getElementById("age").value
    if (Number.isInteger(parseInt(userid))){
        alert('Вы ввели не число')
    }
 if (Number.isInteger(parseInt(userage))){
        alert('Вы ввели не число')
    }
}