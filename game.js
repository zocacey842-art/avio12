let aviatorMultiplier = 1.00;
let aviatorInterval;
let isFlying = false;
let crashPoint;

function startAviator() {
    if (isFlying) return;
    
    // የውርርድ መጠን
    const bet = document.getElementById('aviator-bet-amount').value;
    console.log("Bet placed: " + bet + " ETB");

    // የጨዋታ ሁኔታዎችን አስተካክል
    isFlying = true;
    aviatorMultiplier = 1.00;
    crashPoint = (Math.random() * 3 + 1.1).toFixed(2); // በዘፈቀደ የሚመጣ ክራሽ (1.1 - 4.1)
    
    document.getElementById('bet-btn').style.display = 'none';
    document.getElementById('cashout-btn').style.display = 'block';
    document.getElementById('multiplier-display').style.color = 'white';

    // በረራው ይጀምር
    aviatorInterval = setInterval(() => {
        aviatorMultiplier += 0.01;
        document.getElementById('multiplier-display').innerText = aviatorMultiplier.toFixed(2) + "x";
        
        // አውሮፕላኗን ወደ ላይ አንቀሳቅስ
        const plane = document.getElementById('plane');
        plane.style.left = (aviatorMultiplier * 20) + "px";
        plane.style.bottom = (aviatorMultiplier * 15) + "px";

        // Crash ካደረገ
        if (aviatorMultiplier >= crashPoint) {
            stopFlight(false);
        }
    }, 100);
}

function cashOut() {
    if (!isFlying) return;
    const winAmount = (document.getElementById('aviator-bet-amount').value * aviatorMultiplier).toFixed(2);
    alert("አሸንፈዋል! " + winAmount + " ETB");
    stopFlight(true);
}

function stopFlight(isWin) {
    clearInterval(aviatorInterval);
    isFlying = false;
    
    if (!isWin) {
        document.getElementById('multiplier-display').innerText = "FLEW AWAY!";
        document.getElementById('multiplier-display').style.color = "#ff0044";
    }

    setTimeout(() => {
        document.getElementById('bet-btn').style.display = 'block';
        document.getElementById('cashout-btn').style.display = 'none';
        document.getElementById('multiplier-display').innerText = "1.00x";
        document.getElementById('plane').style.left = "20px";
        document.getElementById('plane').style.bottom = "20px";
    }, 2000);
}
