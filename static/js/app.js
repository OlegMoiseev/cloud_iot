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


        console.log("empted...");
        document.getElementById("trashDate").innerHTML = "Trash at " + Date().toString();

        for (let i = 0; i < result.length; ++i)
        {
            let vars = result[i].split(", ");
            var row = table.insertRow(i+1);  // because we have header of the table
            for (let j = 0; j < vars.length; ++j)
            {
                row.insertCell(j).innerHTML = vars[j];
            }
        }
    };
    xhr.onerror = function () {
        console.log("Some error occurred - msg from onerror func");
    };
    xhr.send();
}
