/// <reference types="vite/client" />
import type { RoutineAPI } from '../shared/types';

declare global {
  interface Window {
    routineAPI?: RoutineAPI;
  }
}
