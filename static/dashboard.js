/**
 * Sets and updates the trip cost based on the current fuel prices and amount of fuel consumed.
 * fuelPrice($/g) * fuelConsumed(g) = tripCost($)
 */
fuelPrice = document.getElementById("fuelPrice");
fuelConsumed = document.getElementById("fuelConsumed");
tripCost = document.getElementById("tripCost");

tripCost.innerText = (fuelPrice.value * fuelConsumed.innerText).toFixed(2);

fuelPrice.addEventListener("change", (e) => {
    tripCost.innerText = (e.target.value * fuelConsumed.innerText).toFixed(2);
});