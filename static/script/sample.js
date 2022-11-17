const fs = require('fs')

$('#editable-select').editableSelect();
const passage = "Leonardo DiCaprio was born on November 11, 1974. He can do acting and producing. He has acted in biopics. His films have earned US$7.2 billion. He has won an Academy Award and three Golden Globe Awards. He was born in Los Angeles. Manchester City Football Club is based in Manchester. It competes in the Premier League. It was known as Ardwick Association Football Club. Manchester City Football Club is referred as The Centurions and The Fourmidables. Its home ground is located in east Manchester. Its home ground is also known as CityofManchesterStadium. Shahrukh Khan was born on November 2, 1965. He has done 111 movies. Virat Kohli was born on November 5, 1988. He plays cricket. He plays for India. He also plays for RCB."
const question = "What can Virat Kohli play?"

$(document).ready(function () {
    $(".passage").text(passage);
});

async function answer(payload) {
    var answers = "Sorry. Model couldn't fetch the answer. Please rephrase or ask a different question."
    fetch('/submit', {
        "method": 'POST',
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify(payload)
    })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            $("#answer").text((data))
            $("button").css("visibility", "visible");
        })
    console.log("answer fn", answers)
}
function buildModel() {
    var data = $(".passage").text()
    fs.writeFile('./content/test.txt', data, (err) => {
        if (err) throw err;
    })
}
function findAnswer() {
    $("#answer").text("");
    const question = $("#editable-select").val() || $("#editable-select").attr('placeholder');
    const passage = document.getElementById("passage").innerText;
    const formData = new FormData();
    payload = {
        'question': question
    };
    console.log(payload)
    answer(payload).then((answers) => {
        console.log("answer", answers)
    })
        .catch(err => {
            alert("Whoops")
            console.error(err)
        });
}
