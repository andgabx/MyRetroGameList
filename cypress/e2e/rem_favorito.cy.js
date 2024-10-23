describe('template spec', () => {
  let name='testes'
  let password='yuri1234'
  before(() =>{
    cy.visit('http://127.0.0.1:8000/login/')
    cy.get('#username').click()
    cy.get('[type="text"]').type(name)
    cy.get('[type="password"]').type(password)
    cy.get('[type="submit"]').click()
    cy.visit('http://127.0.0.1:8000/gamelist/')
    cy.get(':nth-child(3) > .flex-grow > .justify-between > .flex > .px-2 > .bi').click()
  })
  
  it('teste_cadastro', () => {
    cy.visit('http://127.0.0.1:8000/gamelist/')
    cy.get(':nth-child(3) > .flex-grow > .justify-between > .flex > .px-2 > .bi').click()
    cy.get('.w-12').click()
    cy.get(':nth-child(1) > .overflow-x-auto > .flex > .text-white').should('have.text','No games available.')
    
  })
})