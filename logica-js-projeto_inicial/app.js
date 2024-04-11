let numeroAleatoriomax = 10;
let chute
let numero = parseInt(Math.random() * numeroAleatoriomax + 1);
console.log(numero);
let tentativas = 1;

alert('Olá bem vindo ao jogo da advinhação');

while (chute != numero) {
    let chute = prompt(`Digite um numero entre 1 e ${numeroAleatoriomax}`);
    if (chute == numero) {
        break;
    } else {
        if (chute > numero) {
            alert('O numero misterioso é menor!');
        } else {
            alert('O numero misteriosos é maior!');
        }
        tentativas++;
    }
}

let nomeTentativas = tentativas > 1 ? 'tentativas' : 'tentativa'

alert(`Parabéns, você acertou o numero misterioso com ${tentativas} ${nomeTentativas}`)

