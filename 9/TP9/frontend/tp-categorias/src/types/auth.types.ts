export interface UsuarioAuth {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  roles: string[];
}

export interface UsuarioPublic extends UsuarioAuth {
  celular: string | null;
  activo: boolean;
}

export interface RegisterData {
  nombre: string;
  apellido: string;
  email: string;
  celular?: string;
  password: string;
}

export interface MensajeResponse {
  mensaje: string;
}