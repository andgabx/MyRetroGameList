describe('template spec', () => {
  beforeEach(() => {
    cy.visit('/login/')
    cy.get('#username').type('testes')
    cy.get('#password').type('yuri1234')
    cy.get('.bg-purple-600').click()
  })

  it('colocar bio', () => {
    cy.visit('/')
    cy.get('.w-12').click()
    cy.get('#editDescriptionBtn > .shadow-lg').dblclick()
    cy.get('#descriptionInput')
      .clear()
      .type('Teste')
    cy.get('.bg-green-600').click()
  })
})
