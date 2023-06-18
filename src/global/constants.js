export const Constants = {
    HomeView: "home",
    LocationsView: "locations",
    BoxesView: "boxes",
    ProductsView: "products",
    All:  "all"
}

export function resetLangToDefault()
{
    return (navigator.language || navigator.userLanguage).substring(0, 2);
}