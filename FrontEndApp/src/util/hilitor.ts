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

export function removeHighlight() {
    // Find all div elements with the class "input-text-search"
    const divElements = document.querySelectorAll('.input-text-search');

    // Loop through each div element
    divElements.forEach((divElement) => {
        // Find all mark elements inside the current div
        const markElements = divElement.querySelectorAll('mark');

        // Loop through each mark element and replace it with its content
        markElements.forEach((markElement) => {
            const content = markElement.textContent; // Get the content of the mark tag
            const textNode = document.createTextNode(content as string); // Create a new text node with the content
            markElement?.parentNode?.replaceChild(textNode, markElement); // Replace the mark tag with the text node
        });
    });
}
