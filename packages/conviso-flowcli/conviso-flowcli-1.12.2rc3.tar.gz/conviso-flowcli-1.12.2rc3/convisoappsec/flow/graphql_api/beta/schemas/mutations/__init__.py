
CREATE_SAST_FINDING_INPUT = """ 
mutation createSastFinding($input: CreateSastFindingInput!) {
  createSastFinding(input: $input) {
    clientMutationId
    errors
    issue {
      id
    }
  }
}
"""
