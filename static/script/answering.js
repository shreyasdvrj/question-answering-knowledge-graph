// Data
const passage = "Leonardo DiCaprio was born on November 11, 1974. He can do acting and producing. He has acted in biopics. His films have earned US$7.2 billion. He has won an Academy Award and three Golden Globe Awards. He was born in Los Angeles. Manchester City Football Club is based in Manchester. It competes in the Premier League. It was known as Ardwick Association Football Club. Manchester City Football Club is referred as The Centurions and The Fourmidables. Its home ground is located in east Manchester. Its home ground is also known as CityofManchesterStadium. Shahrukh Khan was born on November 2, 1965. He has done 111 movies. Virat Kohli was born on November 5, 1988. He plays cricket. He plays for India. He also plays for RCB."
const question = "What can Virat Kohli play?"

let model = null;
$(document).ready(function(){
  $("#question").attr("placeholder", question);
  $(".passage").text(passage);
});

async function answer() {
  console.log('{{qna_answer}}')
  return {qna_answer};
}

function buttonClick() {
  $("#answer").text("");
  const question = $("#question").val() || $("#question").attr('placeholder');
  const passage = document.getElementById("passage").innerText;
  const formData = new FormData();
  formData.append('question', question);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/submit', true);
  xhr.send(formData);
  answer().then((answers) =>   {
    $("#answer").text(answers)
    $("button").css("visibility", "visible");    
  })
  .catch(err => {
    alert("Whoops")
    console.error(err)
  });
}

$("button").click(buttonClick);