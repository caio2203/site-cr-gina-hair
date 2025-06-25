import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-contato',
  standalone: true,
  imports: [],
  templateUrl: './contato.component.html',
  styleUrl: './contato.component.css'
})
export class ContatoComponent {
  http: any;
  onSubmit(form: NgForm) {
  const dados = {
    nome: form.value.nome,
    telefone: form.value.telefone,
    servico: form.value.servico,
    dataPreferida: form.value.data
  };

  this.http.post('http://localhost:4200/#contato', dados)
    .subscribe({
      next: (res: any) => alert('Mensagem enviada no WhatsApp!'),
      error: () => alert('Erro ao enviar.')
    });
}}
