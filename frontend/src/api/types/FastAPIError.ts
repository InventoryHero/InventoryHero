// simple string error (HTTPException)
interface FastAPIStringError {
  detail: string
}

// validation errors (list of Pydantic errors)
interface FastAPIValidationError {
  detail: {
    loc: (string | number)[]
    msg: string
    type: string
  }[]
}

// union type
export type FastAPIError = FastAPIStringError | FastAPIValidationError
