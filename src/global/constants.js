import {getSettings} from "@/db/dexie";

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

export function colorBurgerBars(theme)
{
    let burger_bars = document.getElementsByClassName("bm-burger-bars");
    for(let i = 0; i < burger_bars.length; ++i)
    {
        let color = "white";
        if(theme === "light-theme")
            color = "black";
        burger_bars[i].style.cssText = "background-color:" +color+ "!important;top: " + i*40 + "%;"
    }
}