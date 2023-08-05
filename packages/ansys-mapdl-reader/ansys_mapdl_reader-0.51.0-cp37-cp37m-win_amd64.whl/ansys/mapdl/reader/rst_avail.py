"""Contains the available result class

Based on resucm.inc included in the standard ANSYS unified install

Current as of v193 (which is the current result file as of v20.2)

**********  AvailData bits  **********
 bit   data item

element data (see elparm.inc)
  1     EMS  - miscellaneous summable items(normally includes face pressures)
  2     ENF  - nodal forces
  3     ENS  - nodal stresses
  4     ENG  - element energies and volume
  5     EGR  - nodal gradients
  6     EEL  - nodal elastic strains
  7     EPL  - nodal plastic strains
  8     ECR  - nodal creep strains
  9     ETH  - nodal thermal strains (includes swelling strains)
 10     EUL  - element euler angles
 11     EFX  - nodal fluxes
 12     ELF  - nodal forces generated by the element, e.g. lorentz or maxwell forces
 13     EMN  - miscellaneous nonsummable items
 14     ECD  - nodal current densities
 15     ENL  - nodal nonlinear items, e.g. equivalent plastic strains
 16     EHC  - element joule heating
 17     EPT  - nodal temperatures
 18     SURF - face surface stresses
 19     EDI  - nodal diffusion strains
 20     ESTR - POST1 element (ETABLE) data
 21     ECT  - nodal contact items, e.g. penetration
 22     EXYZ - integration point locations
 23     EBAC - back stresses(for kinematic hardening)
 24     ESVR - saved variables from usermat
 25     EMR  - element material saved record
 26     ---

nodal data
 27     NSL  - Nodal displacements
 28     VSL  - Nodal velocities
 29     ASL  - Nodal accelerations
 30     RF   - Nodal reaction forces
 31     ---

"""


DESCRIPTION = {
    'EMS': 'miscellaneous summable items(normally includes face pressures)',
    'ENF': 'nodal forces',
    'ENS': 'nodal stresses',
    'ENG': 'element energies and volume',
    'EGR': 'nodal gradients',
    'EEL': 'nodal elastic strains',
    'EPL': 'nodal plastic strains',
    'ECR': 'nodal creep strains',
    'ETH': 'nodal thermal strains (includes swelling strains)',
    'EUL': 'element euler angles',
    'EFX': 'nodal fluxes',
    'ELF': 'nodal forces generated by the element, e.g. lorentz or maxwell forces',
    'EMN': 'miscellaneous nonsummable items',
    'ECD': 'nodal current densities',
    'ENL': 'nodal nonlinear items, e.g. equivalent plastic strains',
    'EHC': 'element joule heating',
    'EPT': 'nodal temperatures',
    'SURF': 'face surface stresses',
    'EDI': 'nodal diffusion strains',
    'ESTR': 'POST1 element (ETABLE) data',
    'ECT': 'nodal contact items, e.g. penetration',
    'EXYZ': 'integration point locations',
    'EBAC': 'back stresses(for kinematic hardening)',
    'ESVR': 'saved variables from usermat',
    # 'EMR': 'element material saved record',
    'NSL': 'Nodal displacements',
    'VSL': 'Nodal velocities',
    'ASL': 'Nodal accelerations',
    'RF': 'Nodal reaction forces',
}


class AvailableResults():

    def __init__(self, avail_bits, is_thermal):
        """Parse the available bits and determine if a given result is
        available.
        """
        self._avail_bits = avail_bits
        self._parsed_bits = {
            'EMS': self.ems,
            'ENF': self.enf,
            'ENS': self.ens,
            'ENG': self.eng,
            'EGR': self.egr,
            'EEL': self.eel,
            'EPL': self.epl,
            'ECR': self.ecr,
            'ETH': self.eth,
            'EUL': self.eul,
            'EFX': self.efx,
            'ELF': self.elf,
            'EMN': self.emn,
            'ECD': self.ecd,
            'ENL': self.enl,
            'EHC': self.ehc,
            'EPT': self.ept,
            'SURF': self.surf,
            'EDI': self.edi,
            'ESTR': self.estr,
            'ECT': self.ect,
            'EXYZ': self.exyz,
            'EBAC': self.ebac,
            'ESVR': self.esvr,
            # 'EMR': self.emr,
            'NSL': self.nsl,
            'VSL': self.vsl,
            'ASL': self.asl,
            'RF': self.rf,
            }

        self._valid_results = []
        for key, value in self._parsed_bits.items():
            if value:
                self._valid_results.append(key)

        self.description = DESCRIPTION
        if is_thermal:
            self.description['NSL'] = 'Nodal temperatures'

    def __getitem__(self, key):
        """Allow a key access"""
        return self._parsed_bits[key]

    def __iter__(self):
        for key in self._valid_results:
            yield key

    @property
    def ems(self):
        """Miscellaneous summable items(normally includes face pressures)"""
        return bool(self._avail_bits & 0b1 << 1)

    @property
    def enf(self):
        """Nodal forces"""
        return bool(self._avail_bits & 0b1 << 2)

    @property
    def ens(self):
        """Nodal stresses"""
        return bool(self._avail_bits & 0b1 << 3)

    @property
    def eng(self):
        """Element energies and volume"""
        return bool(self._avail_bits & 0b1 << 4)

    @property
    def egr(self):
        """Nodal gradients"""
        return bool(self._avail_bits & 0b1 << 5)

    @property
    def eel(self):
        """Nodal elastic strains"""
        return bool(self._avail_bits & 0b1 << 6)

    @property
    def epl(self):
        """Nodal plastic strains"""
        return bool(self._avail_bits & 0b1 << 7)

    @property
    def ecr(self):
        """Nodal creep strains"""
        return bool(self._avail_bits & 0b1 << 8)

    @property
    def eth(self):
        """Nodal thermal strains (includes swelling strains)"""
        return bool(self._avail_bits & 0b1 << 9)

    @property
    def eul(self):
        """Element euler angles"""
        return bool(self._avail_bits & 0b1 << 10)

    @property
    def efx(self):
        """Nodal fluxes"""
        return bool(self._avail_bits & 0b1 << 11)

    @property
    def elf(self):
        """Nodal forces generated by the element, e.g. lorentz or maxwell forces"""
        return bool(self._avail_bits & 0b1 << 12)

    @property
    def emn(self):
        """Miscellaneous nonsummable items"""
        return bool(self._avail_bits & 0b1 << 13)

    @property
    def ecd(self):
        """Nodal current densities"""
        return bool(self._avail_bits & 0b1 << 14)

    @property
    def enl(self):
        """Nodal nonlinear items, e.g. equivalent plastic strains"""
        return bool(self._avail_bits & 0b1 << 15)

    @property
    def ehc(self):
        """Element joule heating"""
        return bool(self._avail_bits & 0b1 << 16)

    @property
    def ept(self):
        """Nodal temperatures"""
        return bool(self._avail_bits & 0b1 << 17)

    @property
    def surf(self):
        """Face surface stresses"""
        return bool(self._avail_bits & 0b1 << 18)

    @property
    def edi(self):
        """Nodal diffusion strains"""
        return bool(self._avail_bits & 0b1 << 19)

    @property
    def estr(self):
        """Post1 element (ETABLE) data"""
        return bool(self._avail_bits & 0b1 << 20)

    @property
    def ect(self):
        """Nodal contact items, e.g. penetration"""
        return bool(self._avail_bits & 0b1 << 21)

    @property
    def exyz(self):
        """Integration point locations"""
        return bool(self._avail_bits & 0b1 << 22)

    @property
    def ebac(self):
        """Back stresses(for kinematic hardening)"""
        return bool(self._avail_bits & 0b1 << 23)

    @property
    def esvr(self):
        """Saved variables from usermat"""
        return bool(self._avail_bits & 0b1 << 24)

    # @property
    # def emr(self):
    #     """Element material saved record"""
    #     return bool(self._avail_bits & 0b1 << 25)

    @property
    def nsl(self):
        """Nodal displacements"""
        return bool(self._avail_bits & 0b1 << 27)

    @property
    def vsl(self):
        """Nodal velocities"""
        return bool(self._avail_bits & 0b1 << 28)

    @property
    def asl(self):
        """Nodal accelerations"""
        return bool(self._avail_bits & 0b1 << 29)

    @property
    def rf(self):
        """Nodal reaction forces"""
        return bool(self._avail_bits & 0b1 << 30)

    def __repr__(self):
        txt = "Available Results:\n"

        if self.ems:
            txt += "EMS : Miscellaneous summable items (normally includes face pressures)\n"
        if self.enf:
            txt += "ENF : Nodal forces\n"
        if self.ens:
            txt += "ENS : Nodal stresses\n"
        if self.eng:
            txt += "ENG : Element energies and volume\n"
        if self.egr:
            txt += "EGR : Nodal gradients\n"
        if self.eel:
            txt += "EEL : Nodal elastic strains\n"
        if self.epl:
            txt += "EPL : Nodal plastic strains\n"
        if self.ecr:
            txt += "ECR : Nodal creep strains\n"
        if self.eth:
            txt += "ETH : Nodal thermal strains (includes swelling strains)\n"
        if self.eul:
            txt += "EUL : Element euler angles\n"
        if self.efx:
            txt += "EFX : Nodal fluxes\n"
        if self.elf:
            txt += "ELF : Nodal forces generated by the element, e.g. lorentz or maxwell forces\n"
        if self.emn:
            txt += "EMN : Miscellaneous nonsummable items\n"
        if self.ecd:
            txt += "ECD : Nodal current densities\n"
        if self.enl:
            txt += "ENL : Nodal nonlinear items, e.g. equivalent plastic strains\n"
        if self.ehc:
            txt += "EHC : Element joule heating\n"
        if self.ept:
            txt += "EPT : Nodal temperatures\n"
        if self.surf:
            txt += "SURF: Face surface stresses\n"
        if self.edi:
            txt += "EDI : Nodal diffusion strains\n"
        if self.estr:
            txt += "ESTR: Post1 element (ETABLE) data\n"
        if self.ect:
            txt += "ECT : Nodal contact items, e.g. penetration\n"
        if self.exyz:
            txt += "EXYZ: Integration point locations\n"
        if self.ebac:
            txt += "EBAC: Back stresses (for kinematic hardening)\n"
        if self.esvr:
            txt += "ESVR: Saved variables from usermat\n"
        # if self.emr:
        #     txt += "EMR : Element material saved record\n"
        if self.nsl:
            txt += "NSL : Nodal displacements\n"
        if self.vsl:
            txt += "VSL : Nodal velocities\n"
        if self.asl:
            txt += "ASL : Nodal accelerations\n"
        if self.rf:
            txt += "RF  : Nodal reaction forces\n"

        return txt
