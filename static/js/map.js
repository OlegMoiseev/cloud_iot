ymaps.ready(function(){
        // Указывается идентификатор HTML-элемента.
    var lat_center = 59.913743;
    var long_center = 29.774067;

    var trash_map = new ymaps.Map("trash_map", {
        center: [lat_center, long_center],
        zoom: 10
    });

    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_all', true);
    xhr.onload = function () {
        var text = xhr.responseText;
        text = text.slice(2, -2);
        var result = text.split("), (");

        for (let i = 0; i < result.length; ++i)
        {
            let vars = result[i].split(", ");
            var lat = parseFloat(vars[2]);
            var long = parseFloat(vars[3]);
            var name_id = vars[0].toString();
            var trash_can = new ymaps.Placemark([lat, long], {
                iconContent: name_id
            });
            trash_map.geoObjects.add(trash_can);
        }
    };
    xhr.onerror = function () {
        console.log("Some error occurred - msg from onerror func");
    };
    xhr.send();
});