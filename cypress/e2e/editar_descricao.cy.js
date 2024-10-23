describe('template spec', () => {

  beforeEach(() => {
      cy.visit('/login/')
      cy.get('#username').type('testes')
      cy.get('#password').type('yuri1234')
      cy.get('.bg-purple-600').click()
  })

  it('edit bio', () => {
    cy.visit('/')
    cy.get('.w-12').click()
    cy.get('#editDescriptionBtn > .shadow-lg').click()
    cy.get('#descriptionInput').type(' e Teste 2')
    cy.get('.bg-green-600').click()
  })
})