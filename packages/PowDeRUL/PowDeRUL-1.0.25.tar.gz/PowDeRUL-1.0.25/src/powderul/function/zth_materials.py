from numpy import convolve
from powderul.function.materials import Materials
from powderul.function.poly_somme import poly_somme

class ZthMaterials:
  """
  Class representing the thermal impedance of materials for IGBT and diode. It uses Foster's model.
  """

  def __init__(self, dic):
    """
    Initializes a ZthMaterials instance. 

    Parameters:
    dic (dict): A dictionary containing thermal resistance and thermal capacitance for IGBT and diode.
    """

    # Extracting values from the dictionary
    self.layers_Rth_IGBT_jc = dic["layers_Rth_jc_IGBT"]
    self.layers_Cth_IGBT_jc = dic["layers_Cth_jc_IGBT"]
    self.layers_Rth_diode_jc = dic["layers_Rth_jc_diode"]
    self.layers_Cth_diode_jc = dic["layers_Cth_jc_diode"]
    self.Rth_ch = dic["Rth_ch"]
    self.Cth_ch = dic["Cth_ch"]
    self.Rth_hf = dic["Rth_hf"]

    self.Num_materials_IGBT = len(self.layers_Rth_IGBT_jc)
    self.Num_materials_diode = len(self.layers_Rth_diode_jc)

    # Initializing remaining properties
    self.num_foster_IGBT = self.den_foster_IGBT = None
    self.num_foster_diode = self.den_foster_diode = None
    self.num_ch = self.den_ch = None
    self.num_hf = self.den_hf = None
    self.num_cf = self.den_cf = None
    self.materials_IGBT = []
    self.materials_diode = []

    # Creating instances of the Materials class
    for i in range(self.Num_materials_IGBT):
      material = Materials(self.layers_Rth_IGBT_jc[i],
                           self.layers_Cth_IGBT_jc[i])
      self.materials_IGBT.append(material)

    for i in range(self.Num_materials_diode):
      material = Materials(self.layers_Rth_diode_jc[i],
                           self.layers_Cth_diode_jc[i])
      self.materials_diode.append(material)


  def calculate_zth_foster(self):
    """
    Calculates thermal impedance using the Foster model.
    """

    num = {}
    den = {}

    # Calculating for IGBT
    for i in range(self.Num_materials_IGBT, 0, -1):
      if i == self.Num_materials_IGBT:
        num[i] = [self.materials_IGBT[i - 1].Rth]
        den[i] = [
          self.materials_IGBT[i - 1].Cth * self.materials_IGBT[i - 1].Rth, 1
        ]
      else:
        num[i] = [self.materials_IGBT[i - 1].Rth]
        den[i] = [
          self.materials_IGBT[i - 1].Cth * self.materials_IGBT[i - 1].Rth, 1
        ]
        num[i] = poly_somme(convolve(den[i + 1], num[i]),
                            convolve(den[i], num[i + 1]))
        den[i] = convolve(den[i + 1], den[i])

    self.num_foster_IGBT = num
    self.den_foster_IGBT = den

    num_diode = {}
    den_diode = {}

    # Calculating for Diode
    for i in range(self.Num_materials_diode, 0, -1):
      if i == self.Num_materials_diode:
        num_diode[i] = [self.materials_diode[i - 1].Rth]
        den_diode[i] = [
          self.materials_diode[i - 1].Cth * self.materials_diode[i - 1].Rth, 1
        ]
      else:
        num_diode[i] = [self.materials_diode[i - 1].Rth]
        den_diode[i] = [
          self.materials_diode[i - 1].Cth * self.materials_diode[i - 1].Rth, 1
        ]
        num_diode[i] = poly_somme(convolve(den_diode[i + 1], num_diode[i]),
                                  convolve(den_diode[i], num_diode[i + 1]))
        den_diode[i] = convolve(den_diode[i + 1], den_diode[i])

    self.num_foster_diode = num_diode
    self.den_foster_diode = den_diode


  def calculate_zth_cf(self):
    """
    Calculate the case-to-fluid thermal impedance.
    """

    self.num_hf = self.Rth_hf
    self.den_hf = 0
    if (self.Cth_ch==0):
      self.num_cf = poly_somme(convolve(self.num_hf, [1]), self.Rth_ch)
      self.den_cf = 1
    else:
      self.num_cf = poly_somme(convolve(self.num_hf, [self.Rth_ch * self.Cth_ch, 1]), self.Rth_ch)
      self.den_cf = [self.Rth_ch * self.Cth_ch, 1]
