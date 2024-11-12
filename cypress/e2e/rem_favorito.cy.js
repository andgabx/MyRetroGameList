describe('template spec', () => {
  let name='testes'
  let password='yuri1234'
  let nomeJogoAdicionado;
  before(() =>{
    cy.visit('/login/')
    cy.get('#username').click()
    cy.get('[type="text"]').type(name)
    cy.get('[type="password"]').type(password)
    cy.get('[type="submit"]').click()

  })
  
  it('teste_remover', () => {
    cy.visit('http://127.0.0.1:8000/gamelist/')
    cy.get('.space-y-4 > :nth-child(1) > :nth-child(2) > .flex > .text-xl')
      .invoke('text')
      .then((text) => {
        nomeJogoAdicionado = text.trim();
      })
    cy.get('#favorite-form-3 > .px-2 > .bi').click()
    cy.wait(4000);
    cy.get('.w-12').click()
    cy.get(':nth-child(1) > .overflow-x-auto > .flex > .flex-shrink-0 > .mt-2').should(($elements) => {
        const nomes = $elements.map((index, el) => Cypress.$(el).text().trim()).get()
        expect(nomes).to.include(nomeJogoAdicionado)
      })
      cy.visit('http://127.0.0.1:8000/gamelist/')
      cy.get('#favorite-form-3 > .px-2 > .bi').click()
    
  })
})

// Ignorar exceções não capturadas de scripts de terceiros
Cypress.on('uncaught:exception', (err, runnable) => {
  // Ignora o erro e não faz o teste falhar
  return false;
})