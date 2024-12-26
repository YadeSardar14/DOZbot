var dooz = [0, 0, 0, 0, 0, 0, 0, 0, 0];
var turn = false;
var tow_game = false;
var game_currenting = false;
var replace_mod = false;
var replace_home = 0;
var User =  new URLSearchParams(window.location.search).get("userid") || 0;

async function AIproccecing(current_dooz) {
    
    try{
    const response = await fetch("/GetAiDoz",{
        method: "POST",
        headers:{ "Content-Type" : "application/json" },
        body: JSON.stringify(current_dooz)
    });

    if (response.ok){
    const result = await response.json();
    dooz = result.AIdooz;
    update_bord(dooz);

}
    else
    console.error("Data Error!");

}   catch(er){

    console.error(er.message);
}}
 




const me = document.getElementById('me');
me.addEventListener('click', function() {
    turn_handler(me);
});

const ai = document.getElementById('ai');
ai.addEventListener('click', function() {
    turn_handler(ai);
});

const tow = document.getElementById('2p');
tow.addEventListener('click', function() {
    turn_handler(tow);
});


(function() {
    hid_show(document.getElementsByClassName('dooz_page')[0])})();

(function() {
    hid_show(document.getElementsByClassName('panel2')[0])})();


function hid_show(HPage, SPage) {

    HPage.style.display = "none";

    for (let element of HPage.elements)
        element.disabled = true;

    if (SPage) {

        SPage.style.display = "block";

        for (let element of SPage.elements)
            element.disabled = false;
    }
}

function update_bord(dooz) {
    
    for (let i = 0; i < 9; i++) {
        const home = document.getElementById(i);
       
        switch (dooz[i]) {
            case 0:
                home.style.removeProperty("background-color");
                break;
            case 1:
                home.style.backgroundColor = "red";
                break;
            case -1:
                home.style.backgroundColor = "green";
                break;
        }
        }}


function claer_bord() {

    dooz = [0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0];

    bord = document.getElementsByClassName('dooz_page')[0];

    for (let element of bord.elements) {
        // element.style.backgroundColor = '#cc00661a';
        element.style.removeProperty("background-color");
        element.style.opacity = '1';
    }
    n = document.getElementById("new");
    n.style.display = 'none';
    n.style.opacity = 0;
    
    game_currenting = false;
    tow_game = false;
    replace_mod = false;
    replace_home =0;

}


function win_efect(w) {

    let remove = [0,
        8,
        6,
        2,
        4,
        7,
        1,
        3,
        5];
    remove = remove.filter(item => (item != w[0][0] && item != w[0][1] && item != w[0][2]));

    let homs = document.getElementsByClassName("dooz_page")[0];
    let newg = document.getElementById("new");


    let delay = 100;
    for (let i of remove) {

        setTimeout(() => {
            homs[i].style.opacity = "0.2"
        }, delay);
        delay += 100;

    }


    for (let element of homs.elements)
        element.disabled = true;

    newg.style.display = 'block';
    newg.disabled = false;
    setTimeout(() => {}, 50);

    for (let i = 0; i < 100; i++) {

        setTimeout(() => {
            newg.style.opacity = i/100;
        }, i*20);
    }

    fetch("/lost",{
        method: "POST",
        headers: { "Content-Type" : "application/json" },
        body: JSON.stringify({"userid" : User, "dooz" : dooz , "type" : tow_game})}).catch(()=>{console.log("Lost Request ERROR!"); });

}


function ErrorShow(text){

    
    let e = document.getElementById("show");
    e.classList.remove("hid");
    void e.offsetWidth;
    e.classList.add("vis");
    
    e.innerHTML = text;
    
    e.classList.add("hid");
}


function turn_handler(ob) {
    if (ob.id === "me")
        turn = false;
    else if (ob.id === "ai"){
        turn = true;
        AIproccecing(dooz).then(() => {
            turn = false;
        });
    }
    else if (ob.id === '2p')
        tow_game = true;
}

function dooz_handlear(ob) {
    
    if (!game_currenting){
        let cuont = 0;
        for (let h of dooz){
            if (h==0)
            cuont ++;
            if (cuont>3)
            break
        }
        if (cuont < 4)
        game_currenting = true;
    }
    
    if (!game_currenting){
    if (dooz[ob.id]!=0){
       ErrorShow("لطفا یکی از خانه های خود را انتخاب کنید");
        return;
    }}
    else{
        
        if ((dooz[ob.id]==0 || (dooz[ob.id]==1 && !turn) || (dooz[ob.id]==-1 && turn)) && !replace_mod){
            ErrorShow(" یکی از خانه های خود را جهت جابه‌جایی انتخاب کنید");
            return;
        }
        
        else if (replace_mod && ob.id!= replace_home.id && dooz[ob.id]!= 0){
            ErrorShow("لطفا یکی از خانه های خالی را انتخاب کنید");
            return;
        }
        
    }


//-----------------

    if ((game_currenting && !tow_game && !turn) || (game_currenting && tow_game)){
            if (!replace_mod){
                replace_home = ob;
                ob.style.opacity = "0.4";
                replace_mod = true;
            }
            else {
            
                replace_home.style.opacity = "1";
                replace_home.style.removeProperty("background-color");
                dooz[replace_home.id] = 0;
                
                if (turn){
                ob.style.backgroundColor= 'red' ;
                dooz[ob.id] = 1;
                }
                else{
                ob.style.backgroundColor= 'green' ;
                dooz[ob.id] = -1;
                }
                
                if(ob.id != replace_home.id){
                
                if (!tow_game && !turn){
                AIproccecing(dooz).then(()=>{
                    turn = false;
                    let w = win_check(dooz);
                    if (w)
                    win_efect(w);
                     });
                    }
                else
                turn = !turn; }

                
                replace_home = 0;
                replace_mod = false;
            
                
            }
            
        }

    else if (!tow_game && !turn) {

            ob.style.backgroundColor = "green";
            dooz[ob.id] = -1;
            turn = true;

            let w = win_check(dooz);
            if (w)
            win_efect(w);
            
            AIproccecing(dooz).then(()=>{
                turn = false;
                let w = win_check(dooz);
                if (w)
                win_efect(w);
                 });

    } else {

        if (!turn) {
            
            ob.style.backgroundColor = "green";
            dooz[ob.id] = -1;
            turn = true;
            
        } else {
            ob.style.backgroundColor = "red";
            dooz[ob.id] = 1;
            turn = false;
        }

    }


let w = win_check(dooz);
            if (w) {
                win_efect(w);
                //claer_bord();
            }

}


var win_modes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
win_check(dooz)

function win_check(dooz) {

    for (n of win_modes) {

        if (dooz[n[0]] == dooz[n[1]] && dooz[n[1]] == dooz[n[2]] && dooz[n[0]] != 0)
            return [n,
            dooz[n[0]]];

    }

    return 0;

}