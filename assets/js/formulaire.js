function verifcreer(mdp,mdp2)
{
    // Récupérer les valeurs des champs
    var id = document.creer_compte.userid.value;
    var tel= document.creer_compte.phone.value;


    // Supprimer les espaces des valeurs des champs
    id = id.replace(/\s/g, "");
    tel = tel.replace(/\s/g, "");

    // Vérifier la longueur de l'identifiant
    if(id.length < 8 || isNaN(id) )
    {
        alert('Veuillez saisir correctement votre numéro d\'identité');
        document.creer_compte.userid.focus();
        return false;
    }
    // Vérifier la longueur du numéro de téléphone
    else if(tel.length < 8 || isNaN(tel))
    {
        alert('Veuillez saisir correctement votre numéro de téléphone');
        document.creer_compte.phone.focus();
        return false;
    }
    else
    {
        // Expression régulière pour vérifier le mot de passe
        var cont = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[*&#!($)_!]).{8,}$/;

        // Vérifier la longueur du mot de passe
        if(mdp.value.length < 8)
        {
            alert('Le mot de passe doit contenir au moins 8 caractères !');
            mdp.focus();
            return false;
        }
        // Vérifier la complexité du mot de passe
        else if(!cont.test(mdp.value))
        {
            alert("Le mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial parmi '&#!($)_!' !");
            mdp.focus();
            return false;
        }
        // Vérifier que les deux mots de passe correspondent
        else if(mdp2.value != mdp.value)
        {
            alert("Les mots de passe ne correspondent pas !");
            mdp2.focus();
            return false;
        }
        else
        {
            return true;
        }
    }
}
