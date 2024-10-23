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
  
  it('teste_cadastro', () => {
    cy.visit('http://127.0.0.1:8000/gamelist/')
    cy.get(':nth-child(2) > .flex-grow > .flex > div > .text-xl')
      .invoke('text')
      .then((text) => {
        nomeJogoAdicionado = text.trim();
      })
    cy.get(':nth-child(2) > .flex-grow > .justify-between > .flex > .px-2').click()
    cy.get('.w-12').click()
    cy.get(':nth-child(1) > .overflow-x-auto > .flex > .flex-shrink-0 > .mt-2').should(($elements) => {
        const nomes = $elements.map((index, el) => Cypress.$(el).text().trim()).get()
        expect(nomes).to.include(nomeJogoAdicionado)
      })
    
  })
  after(() =>{
    cy.visit('http://127.0.0.1:8000/gamelist/')
    cy.get(':nth-child(2) > .flex-grow > .justify-between > .flex > .px-2').click()


  })
})