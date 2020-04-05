function getInfoAll() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_all', true);
    xhr.onload = function () {
        var text = xhr.responseText;
        text = text.slice(2, -2);
        var result = text.split("), (");

        var table = document.getElementById("myTable");

        var tableHeaderRowCount = 1;
        var rowCount = table.rows.length;
        for (var i = tableHeaderRowCount; i < rowCount; i++) {
            table.deleteRow(tableHeaderRowCount);
        }
        document.getElementById("trashDate").innerHTML = "Trash at " + Date().toString();
        document.getElementById("totalTrashes").innerHTML = String(result.length);
        let countFull = 0;
        let sumFullnesses = 0;
        for (let i = 0; i < result.length; ++i)
        {
            let vars = result[i].split(", ");
            var row = table.insertRow(i+1);  // because we have header of the table
            sumFullnesses += parseInt(vars[1]);
            if (parseInt(vars[1]) > 50)
            {
                ++countFull;
            }
            for (let j = 0; j < vars.length; ++j)
            {
                row.insertCell(j).innerHTML = vars[j];
            }
        }

        document.getElementById("filledTrashes").innerHTML = String(countFull);
        document.getElementById("freeTrashes").innerHTML = String(result.length - countFull);
        document.getElementById("averageLoading").innerHTML = String((sumFullnesses / result.length).toFixed(1)) + '%';

    };
    xhr.onerror = function () {
        console.log("Some error occurred - msg from onerror func");
    };
    xhr.send();
}

let timerReload = setInterval(getInfoAll, 1000);