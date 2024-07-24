


function hover(element, id) {
    switch(id){
        case 0:
            element.setAttribute('src', 'modeled_images/arabic_sign.jpg');
            break
        case 1:
            element.setAttribute('src', 'modeled_images/euro_sign.jpg');
            break
        case 2:
            element.setAttribute('src', 'modeled_images/korean_sign.jpeg');
            break
        case 3:
            element.setAttribute('src', 'modeled_images/stop_sign.jpg');
            console.log("STOP")
            break

    }
}

function unhover(element, id) {
    switch(id){
        case 0:
            element.setAttribute('src', 'img/arabic_sign.jpg');
            break
        case 1:
            element.setAttribute('src', 'img/euro_sign.jpg');
            break
        case 2:
            element.setAttribute('src', 'img/korean_sign.jpeg');
            break
        case 3:
            element.setAttribute('src', 'img/stop_sign.jpg');
            break

    }
}