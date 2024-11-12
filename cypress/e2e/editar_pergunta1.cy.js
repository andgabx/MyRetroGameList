describe('template spec', () => {
    beforeEach(() => {
        cy.visit('/login/')
        cy.get('#username').type('testes')
        cy.get('#password').type('yuri1234')
        cy.get('.bg-purple-600').click()
        cy.visit('http://127.0.0.1:8000/forum/')
        cy.get('[href="/forum/1/"] > .h-48 > .w-full').click()
        cy.get('.mb-8 > input.w-full').type('teste')
        cy.get('.mb-8 > textarea.w-full').type('teste detalhes')
        cy.get('.mb-8 > .px-4').click()
        cy.get('.bg-gray-800 > .text-xl').last().should('have.text', 'teste')
      })
  
    it('editar pergunta', () => {
      
      cy.get('.text-yellow-500').last().click()
      cy.get('#editQuestionTitle').clear().type('teste editado')
      cy.get('#editQuestionDetails').clear().type('detalhes editados')
      cy.get('#editQuestionForm > .px-4').click()
      cy.get('.bg-gray-800 > .text-xl').last().should('have.text', 'teste editado')


    })
    afterEach(() => {
        cy.get('.text-red-500').first().click()
      })
  })
  