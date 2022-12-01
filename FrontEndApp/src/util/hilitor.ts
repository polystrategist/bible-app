/**
 * This will highlight the searched text.
 * @param className
 * @param searched
 */
export function highlighter(className: string, searched: string) {
    if (searched && searched !== '') {
        let divElements = document.getElementsByClassName(className);

        for (const theSearchDiv of Array.from(divElements)) {
            let text = theSearchDiv.innerHTML;
            let re = new RegExp(searched, 'i'); // search for all instances
            let newText = text?.replace(re, `<mark>${searched}</mark>`);
            theSearchDiv.innerHTML = newText;
        }
    }
}
