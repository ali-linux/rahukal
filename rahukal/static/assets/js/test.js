const search = document.getElementById("search");
const matchList = document.getElementById("match-list");

const getCities = async () => {
  const res = await fetch("static/assets/json/cities.json");
  const cities = await res.json();
  localStorage.setItem("cities", JSON.stringify(cities));
};
if (localStorage.getItem("cities") === null) {
  getCities();
}
// Search states.json and filter it
const searchCities = async (searchText) => {
  const cities = JSON.parse(localStorage.getItem("cities"));
  // GEt matched to current text input
  let matches = cities.filter((city) => {
    const regex = new RegExp(`^${searchText}`, "gi");
    return city.name.match(regex);
  });
  if (search.value.length === 0) {
    matchList.innerHTML = " ";
  } else {
    outPutHtml(matches);
  }
};
// const bb = document.getElementById("options");
// bb.addEventListener("hover", selectedOne);
// Show results in HTML
const kk = false;
const outPutHtml = (matches) => {
  if (matches.length > 0) {
    let i = 0;
    let j = 0;
    const html = matches
      .slice(0, 20)
      .map(
        (match) => `
    <div class= "st">
    <input id="option" type='hidden' name='city${(i = i + 1)}'  value='${
          match.name
        }'></input>
    <button id="option${(j =
      j +
      1)}" onclick="selectedOne(this.id)" type='submit' name='test' value='${
          match.name
        }, ${match.country}'>${match.name}, ${match.country}</button>
    </div>
    `
      )
      .join("");
    matchList.innerHTML = html;
  }
};
function selectedOne(id) {
  const a = document.getElementById(id);
  search.value = a.value;
}
search.addEventListener("input", () => {
  searchCities(search.value);
});
