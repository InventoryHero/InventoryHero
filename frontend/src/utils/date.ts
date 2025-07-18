// src/utils/date.ts

/**
 * Converts a Date object to a 'YYYY-MM-DD' string,
 * correctly handling the user's local timezone.
 */
export function toISODateString(date: Date | null): string | null {
    if (!date) return null;

    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
}