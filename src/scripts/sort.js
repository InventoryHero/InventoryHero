export function rankBoxesBySearch(boxes, search) {
    if (search == "") {
        return rankBoxesAlphabetically(boxes);
    }
    let ranking = []

    for (let b = 0; b < boxes.length; b++) {
        let curr_score = 0;
        let curr_score_index = 0;
        for (let w = 0; w < boxes[b].name.length && curr_score_index < search.length; w++) {
            if (boxes[b].name[w].toLowerCase() == search[curr_score_index].toLowerCase()) {
                curr_score_index += 1;
                curr_score += 1;
            }
        }
        //create object
        ranking.push({
            score: curr_score,
            data: boxes[b]
        });
    }

    ranking.sort((a,b) => b.score - a.score); 
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;    
}



function rankBoxesAlphabetically(boxes) {
    let ranking = []

    for (let p = 0; p < boxes.length; p++) {
        if (boxes[p].name.length == 0) {
            ranking.push({
                score: 0,
                data: boxes[p]
            })
            continue;
        }

        ranking.push({
            score: boxes[p].name.toLowerCase().charCodeAt(0) + (boxes[p].starred ? 0 : 1000),
            data: boxes[p]
        })
    }
    ranking.sort((a,b) => a.score - b.score); 
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;
}


// ------------------------


export function rankLocationsBySearch(locations, search) {
    if (search == "") {
        return rankLocationsAlphabetically(locations);
    }
    let ranking = []

    for (let b = 0; b < locations.length; b++) {
        let curr_score = 0;
        let curr_score_index = 0;
        for (let w = 0; w < locations[b].name.length && curr_score_index < search.length; w++) {
            if (locations[b].name[w].toLowerCase() == search[curr_score_index].toLowerCase()) {
                curr_score_index += 1;
                curr_score += 1;
            }
        }
        //create object
        ranking.push({
            score: curr_score,
            data: locations[b]
        });
    }

    ranking.sort((a,b) => b.score - a.score); 
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;    
}



function rankLocationsAlphabetically(locations) {
    let ranking = []


    for (let p = 0; p < locations.length; p++) {
        if (locations[p].name.length == 0) {
            ranking.push({
                score: 0,
                data: locations[p]
            })
            continue;
        }

        ranking.push({
            score: locations[p].name.toLowerCase().charCodeAt(0) + (locations[p].starred ? 0 : 1000),
            data: locations[p]
        })
    }
    ranking.sort((a,b) => a.score - b.score); 
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;
}


// ------------------------


export function rankProductsBySearch(products, search) {
    if (search == "") {
        return rankLocationsAlphabetically(products);
    }
    let ranking = []

    for (let b = 0; b < products.length; b++) {
        let curr_score = 0;
        let curr_score_index = 0;
        for (let w = 0; w < products[b].name.length && curr_score_index < search.length; w++) {
            if (products[b].name[w].toLowerCase() == search[curr_score_index].toLowerCase()) {
                curr_score_index += 1;
                curr_score += 1;
            }
        }
        //create object
        ranking.push({
            score: curr_score,
            data: products[b]
        });
    }

    ranking.sort((a,b) => b.score - a.score);
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;
}



function rankProductsAlphabetically(products) {
    let ranking = []


    for (let p = 0; p < products.length; p++) {
        if (products[p].name.length == 0) {
            ranking.push({
                score: 0,
                data: products[p]
            })
            continue;
        }

        ranking.push({
            score: products[p].name.toLowerCase().charCodeAt(0) + (products[p].starred ? 0 : 1000),
            data: products[p]
        })
    }
    ranking.sort((a,b) => a.score - b.score);
    for (let i = 0; i < ranking.length; i++) {
        ranking[i] = ranking[i].data;
    }
    return ranking;
}