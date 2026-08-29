package org.jcr.usuariosenmemoria.config;


import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("API de Gestión de Estudiantes")
                        .description("Esta API permite administrar estudiantes, cursos y matrículas.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Juan Cruz Robledo")
                                .email("juan.robledo@tuinstituto.edu.ar")
                                .url("https://juancruz.edu.ar"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("http://springdoc.org")));
    }
}