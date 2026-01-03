document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('keyup', (event) => {

        if (event.target.name.includes("percentage")) {
            let percentage_sum = 0

            for (let i = 1; i < event.target.parentElement.parentNode.parentNode.rows.length - 2; i++) {
                let value = event.target.parentElement.parentNode.parentNode.rows[i].cells[2].childNodes[1].value
                if (value) {
                    percentage_sum += Number(value)
                }
            }
            if (100 - percentage_sum > 0) {
                event.target.parentElement.parentNode.parentNode.rows[0].cells[2].childNodes[1].value = 100 - percentage_sum;
            }
            else {
                event.target.parentElement.parentNode.parentNode.rows[0].cells[2].childNodes[1].value = 0;
            }
        }
    });

}, false);

document.addEventListener('formset:edit', (event) => {
    if (event.detail.formsetName === 'author_set') {
        // Do something
    }
});
document.addEventListener('formset:removed', (event) => {
    // Row removed
});