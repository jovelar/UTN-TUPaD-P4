package com.ovelar.P4.Tp1.Exceptions;

import com.ovelar.P4.Tp1.Dto.error.ErrorDTO;
import com.ovelar.P4.Tp1.Dto.error.ErrorDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorDTO>handleValidationException(MethodArgumentNotValidException ex){
        List<String> detalles = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(error -> "El campo '" + error.getField() + "' " + error.getDefaultMessage())
                .toList();

        ErrorDTO error = new ErrorDTO(
                LocalDateTime.now(),
                400,
                "Error de validación",
                detalles
        );

        return ResponseEntity
                .badRequest()
                .body(error);
    }
    @ExceptionHandler(NullPointerException.class)
    public ResponseEntity<ErrorDTO> handleNotFound(NullPointerException ex) {
        ErrorDTO errorDTO = ErrorDTO.simple(HttpStatus.NOT_FOUND.value(),
                "Recurso no encontrado", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorDTO);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorDTO> handleGeneric(Exception ex) {
        ErrorDTO errorDTO = ErrorDTO.simple(HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Error interno del servidor", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorDTO);
    }
}


