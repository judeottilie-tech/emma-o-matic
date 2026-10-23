const coinsDisplay = document.getElementById("coins");
const message = document.getElementById("message");
const dispensed = document.getElementById("dispensed");

function coinWord(count) {
  return Number(count) === 1 ? "coin" : "coins";
}

async function loadStock() {
  const response = await fetch("/inventory");
  const stock = await response.json();

  stock.forEach((count, i) => {
    document.getElementById(`stock-${i + 1}`).textContent = count;
  });
}
async function insertCoin() {
  const response = await fetch("/", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ coin: 1 }),
  });
  const coins = response.headers.get("X-Coins");
  coinsDisplay.textContent = coins;
  message.textContent = `Coin inserted. ${coins} total.`;
}

async function returnCoins() {
  const response = await fetch("/", { method: "DELETE" });
  const returned = response.headers.get("X-Coins");
  coinsDisplay.textContent = 0;
  message.textContent = `${returned} ${coinWord(returned)} returned.`;
}

async function buy(id) {
  const response = await fetch(`/inventory/${id}`, { method: "PUT" });
  const coins = response.headers.get("X-Coins");

  if (response.status === 200) {
    const remaining = response.headers.get("X-Inventory-Remaining");
    document.getElementById(`stock-${id}`).textContent = remaining;
    coinsDisplay.textContent = 0;
    message.textContent = `Enjoy drink ${id}! ${coins} ${coinWord(coins)} returned.`;
    const can = document.createElement("div");
    can.className = `can can-${id}`;
    dispensed.appendChild(can);
  } else if (response.status === 403) {
    const needed = 2 - Number(coins);
    const word = needed === 1 ? "quarter" : "quarters";
    message.textContent = `Not enough coins. Insert ${needed} more ${word}.`;
  } else if (response.status === 404) {
    message.textContent = `Drink ${id} is sold out.`;
  }
}

document
  .getElementById("insert-coin")
  .addEventListener("click", insertCoin);
document
  .getElementById("return-coins")
  .addEventListener("click", returnCoins);
document.getElementById("buy-1").addEventListener("click", () => buy(1));
document.getElementById("buy-2").addEventListener("click", () => buy(2));
document.getElementById("buy-3").addEventListener("click", () => buy(3));

loadStock();
