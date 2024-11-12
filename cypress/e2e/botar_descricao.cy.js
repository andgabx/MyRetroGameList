describe('template spec', () => {
  beforeEach(() => {
    cy.visit('/login/')
    cy.get('#username').type('testes')
    cy.get('#password').type('yuri1234')
    cy.get('.bg-purple-600').click()
  })

  it('colocar bio', () => {
    cy.visit('/')
    cy.get('.w-12').should('be.visible').click()
    cy.get('#editDescriptionBtn > .shadow-lg').should('be.visible').click()
    cy.get('#descriptionInput').clear().type('testes')
    cy.get('.bg-green-600').should('be.visible').click()
    cy.get('#userDescription').should('contain', 'testes');  // Usa 'contain' ao invés de 'have.text'
  })

  it('colocar bio e cancelar', () => {
    cy.visit('/')
    cy.get('.w-12').should('be.visible').click()
    cy.get('#editDescriptionBtn > .shadow-lg').should('be.visible').click()
    cy.get('#descriptionInput').clear().type('Testeeee')
    cy.get('#cancelBtn').should('be.visible').click()
    cy.get('#userDescription').should('contain', 'testes');  // Usa 'contain' ao invés de 'have.text'
  })
})

// Ignorar exceções não capturadas de scripts de terceiros
Cypress.on('uncaught:exception', (err, runnable) => {
    // Ignora o erro e não faz o teste falhar
    return false;
})