package com.ovelar.P4.Tp1.Exceptions;

import com.ovelar.P4.Tp1.Dto.error.ErrorDTO;
import com.ovelar.P4.Tp1.Dto.error.ErrorDTO;
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
}


