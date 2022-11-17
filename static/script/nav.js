// nav toggle
document.querySelector('nav .container .nav-toggle').addEventListener('click',()=>{
    document.querySelector('nav .container .nav-toggle span').classList.toggle('active')
    document.querySelector('nav .container .nav-links').classList.toggle('active')
})
document.querySelector('nav .container .nav-links ul li a').addEventListener('click',()=>{
    document.querySelector('nav .container .nav-toggle span').classList.toggle('active')
    document.querySelector('nav .container .nav-links').classList.toggle('active')
})