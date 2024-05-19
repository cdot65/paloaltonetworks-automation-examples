import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";

export function ipv4Validator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const ipv4Regex =
            /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipv4Regex.test(control.value) ? null : { ipv4Invalid: true };
    };
}

export function ipv6Validator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const ipv6Regex = /([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}/;
        return ipv6Regex.test(control.value) ? null : { ipv6Invalid: true };
    };
}

export function domainValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const domainRegex = /^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.[A-Za-z]{2,6}$/;
        return domainRegex.test(control.value) ? null : { domainInvalid: true };
    };
}

export function ipv4SubnetValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const subnetRegex =
            /^(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)$/;
        return subnetRegex.test(control.value) ? null : { subnetInvalid: true };
    };
}

export function ipv4WildcardMaskValidator(): ValidatorFn {
    return (control: AbstractControl): ValidationErrors | null => {
        const wildcardMaskRegex =
            /^(0|128|192|224|240|248|252|254|255)\.(0|128|192|224|240|248|252|254|255)\.(0|128|192|224|240|248|252|254|255)\.(0|128|192|224|240|248|252|254|255)$/;
        return wildcardMaskRegex.test(control.value)
            ? null
            : { wildcardMaskInvalid: true };
    };
}

export const networkValidators = {
    ipv4: ipv4Validator,
    ipv6: ipv6Validator,
    domain: domainValidator,
    subnet: ipv4SubnetValidator,
    wildcardMask: ipv4WildcardMaskValidator,
};
