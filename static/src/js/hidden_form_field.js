function test() {
    if (document.getElementById('transporteselect').value == 'bici') {
        document.getElementById('vacantes').style.display = 'none';
    } else {
        document.getElementById('vacantes').style.display = 'block';
    }
}
