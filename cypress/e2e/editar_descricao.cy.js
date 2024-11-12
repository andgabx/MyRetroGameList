describe('template spec', () => {
  beforeEach(() => {
    cy.visit('/login/')
    cy.get('#username').type('testes')
    cy.get('#password').type('yuri1234')
    cy.get('.bg-purple-600').click()
  })

  it('editar descrição', () => {
    cy.visit('/')
    cy.get('.w-12').should('be.visible').click()
    cy.get('#editDescriptionBtn > .shadow-lg').should('be.visible').click()

    
    cy.get('#descriptionInput').clear().type('Descrição editada')
    cy.get('.bg-green-600').should('be.visible').click()

    
    cy.get('#userDescription').should('contain', 'Descrição editada')
  })

  it('editar e cancelar a descrição', () => {
    cy.visit('/')
    cy.get('.w-12').should('be.visible').click()
    cy.get('#editDescriptionBtn > .shadow-lg').should('be.visible').click()

    
    cy.get('#userDescription').invoke('text').then((originalDescription) => {
      cy.get('#descriptionInput').clear().type('Descrição temporária')
      cy.get('#cancelBtn').should('be.visible').click()
      cy.get('#userDescription').should('contain', originalDescription)
    })
  })
})


Cypress.on('uncaught:exception', (err, runnable) => {
    return false;
})
