//code pour demander confirmation à l'utilisateur lors de la deconnection 
function togleDisconnect()
{
button = document.getElementById('disconnect');
if(button){
    button.addEventListener('click',(event) => {
        let ok = confirm('voulez vous vraiment vous déconnecter ?')
        if(ok){
        alert('déconnection effectuer')
        } else {
        event.preventDefault()
        }
    })
    }
}

window.addEventListener('load',togleDisconnect)