from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    REAL,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint

Base = declarative_base()


class test(Base):
    __tablename__ = "test"

    test_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    test_val1 = Column(Integer, comment="test_val1")
    test_val2 = Column(REAL, comment="test_val2")
    test_val3 = Column(String, comment="test_val3")
    test_val4 = Column(DateTime, comment="test_val4")

    def __init__(self, test_val1, test_val2, test_val3, test_val4):
        self.test_val1 = test_val1
        self.test_val2 = test_val2
        self.test_val3 = test_val3
        self.test_val4 = test_val4


## observational condition ##


class pfs_visit(Base):
    """Tracks the Gen2 visit identifier.
    This is the fundamental identifier for all instrument exposures (MCS, AGC, SPS)
    <<<<< copied from opDB models.py >>>>>
    """

    __tablename__ = "pfs_visit"

    pfs_visit_id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    pfs_visit_description = Column(String)
    pfs_design_id = Column(BigInteger)
    issued_at = Column(DateTime, comment="Issued time [YYYY-MM-DDThh:mm:ss]")

    def __init__(self, pfs_visit_id, pfs_visit_description, pfs_design_id, issued_at):
        self.pfs_visit_id = pfs_visit_id
        self.pfs_visit_description = pfs_visit_description
        self.pfs_design_id = pfs_design_id
        self.issued_at = issued_at


class seeing(Base):
    """Statistics of seeing during a single SpS exposure"""

    __tablename__ = "seeing"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    seeing_mean = Column(REAL, comment="seeing FWHM mean (arcsec.)")
    seeing_median = Column(REAL, comment="seeing FWHM median (arcsec.)")
    seeing_sigma = Column(REAL, comment="seeing FWHM sigma (arcsec.)")
    wavelength_ref = Column(REAL, comment="the reference wavelength to measure the seeing (nm)")

    def __init__(
        self,
        pfs_visit_id,
        seeing_mean,
        seeing_median,
        seeing_sigma,
        wavelength_ref,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.seeing_mean = seeing_mean
        self.seeing_median = seeing_median
        self.seeing_sigma = seeing_sigma
        self.wavelength_ref = wavelength_ref


class seeing_agc_exposure(Base):
    """Statistics of seeing during a single AGC exposure"""

    __tablename__ = "seeing_agc_exposure"
    __table_args__ = (UniqueConstraint("pfs_visit_id", "agc_exposure_id"), {})

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        autoincrement=False,
    )
    agc_exposure_id = Column(Integer, autoincrement=False)
    seeing_mean = Column(REAL, comment="seeing FWHM mean (arcsec.)")
    seeing_median = Column(REAL, comment="seeing FWHM median (arcsec.)")
    seeing_sigma = Column(REAL, comment="seeing FWHM sigma (arcsec.)")
    wavelength_ref = Column(REAL, comment="the reference wavelength to measure the seeing (nm)")
    taken_at = Column(
        DateTime,
        comment="The time at which the exposure was taken [YYYY-MM-DDThh-mm-sss]",
    )

    def __init__(
        self,
        pfs_visit_id,
        agc_exposure_id,
        seeing_mean,
        seeing_median,
        seeing_sigma,
        wavelength_ref,
        taken_at,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.agc_exposure_id = agc_exposure_id
        self.seeing_mean = seeing_mean
        self.seeing_median = seeing_median
        self.seeing_sigma = seeing_sigma
        self.wavelength_ref = wavelength_ref
        self.taken_at = taken_at


class transparency(Base):
    """Statistics of transparency during a single SpS exposure"""

    __tablename__ = "transparency"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    transparency_mean = Column(REAL, comment="transparency mean")
    transparency_median = Column(REAL, comment="transparency median")
    transparency_sigma = Column(REAL, comment="transparency sigma")
    wavelength_ref = Column(REAL, comment="the reference wavelength to measure the transparency (nm)")

    def __init__(
        self,
        pfs_visit_id,
        transparency_mean,
        transparency_median,
        transparency_sigma,
        wavelength_ref,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.transparency_mean = transparency_mean
        self.transparency_median = transparency_median
        self.transparency_sigma = transparency_sigma
        self.wavelength_ref = wavelength_ref


class transparency_agc_exposure(Base):
    """Statistics of transparency during a single AGC exposure"""

    __tablename__ = "transparency_agc_exposure"
    __table_args__ = (UniqueConstraint("pfs_visit_id", "agc_exposure_id"), {})

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        autoincrement=False,
    )
    agc_exposure_id = Column(Integer, primary_key=True, autoincrement=False)
    transparency_mean = Column(REAL, comment="transparency mean")
    transparency_median = Column(REAL, comment="transparency median")
    transparency_sigma = Column(REAL, comment="transparency sigma")
    wavelength_ref = Column(REAL, comment="the reference wavelength to measure the transparency (nm)")
    taken_at = Column(
        DateTime,
        comment="The time at which the exposure was taken [YYYY-MM-DDThh-mm-sss]",
    )

    def __init__(
        self,
        pfs_visit_id,
        agc_exposure_id,
        transparency_mean,
        transparency_median,
        transparency_sigma,
        wavelength_ref,
        taken_at,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.agc_exposure_id = agc_exposure_id
        self.transparency_mean = transparency_mean
        self.transparency_median = transparency_median
        self.transparency_sigma = transparency_sigma
        self.wavelength_ref = wavelength_ref
        self.taken_at = taken_at


class throughput(Base):
    """Total throughput for the visit"""

    __tablename__ = "throughput"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    throughput_b_mean = Column(REAL, comment="the total throughput in b-arm (mean)")
    throughput_b_median = Column(REAL, comment="the total throughput in b-arm (median)")
    throughput_b_sigma = Column(REAL, comment="the total throughput in b-arm (sigma)")
    wavelength_ref_b = Column(REAL, comment="the reference wavelength to measure the total throughput (nm)")
    throughput_r_mean = Column(REAL, comment="the total throughput in r-arm (mean)")
    throughput_r_median = Column(REAL, comment="the total throughput in r-arm (median)")
    throughput_r_sigma = Column(REAL, comment="the total throughput in r-arm (sigma)")
    wavelength_ref_r = Column(REAL, comment="the reference wavelength to measure the total throughput (nm)")
    throughput_n_mean = Column(REAL, comment="the total throughput in n-arm (mean)")
    throughput_n_median = Column(REAL, comment="the total throughput in n-arm (median)")
    throughput_n_sigma = Column(REAL, comment="the total throughput in n-arm (sigma)")
    wavelength_ref_n = Column(REAL, comment="the reference wavelength to measure the total throughput (nm)")
    throughput_m_mean = Column(REAL, comment="the total throughput in m-arm (mean)")
    throughput_m_median = Column(REAL, comment="the total throughput in m-arm (median)")
    throughput_m_sigma = Column(REAL, comment="the total throughput in m-arm (sigma)")
    wavelength_ref_m = Column(REAL, comment="the reference wavelength to measure the total throughput (nm)")

    def __init__(
        self,
        pfs_visit_id,
        throughput_b_mean,
        throughput_b_median,
        throughput_b_sigma,
        wavelength_ref_b,
        throughput_r_mean,
        throughput_r_median,
        throughput_r_sigma,
        wavelength_ref_r,
        throughput_n_mean,
        throughput_n_median,
        throughput_n_sigma,
        wavelength_ref_n,
        throughput_m_mean,
        throughput_m_median,
        throughput_m_sigma,
        wavelength_ref_m,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.throughput_b_mean = throughput_b_mean
        self.throughput_b_median = throughput_b_median
        self.throughput_b_sigma = throughput_b_sigma
        self.wavelength_ref_b = wavelength_ref_b
        self.throughput_r_mean = throughput_r_mean
        self.throughput_r_median = throughput_r_median
        self.throughput_r_sigma = throughput_r_sigma
        self.wavelength_ref_r = wavelength_ref_r
        self.throughput_n_mean = throughput_n_mean
        self.throughput_n_median = throughput_n_median
        self.throughput_n_sigma = throughput_n_sigma
        self.wavelength_ref_n = wavelength_ref_n
        self.throughput_m_mean = throughput_m_mean
        self.throughput_m_median = throughput_m_median
        self.throughput_m_sigma = throughput_m_sigma
        self.wavelength_ref_m = wavelength_ref_m


class noise(Base):
    """Background noise level for the visit"""

    __tablename__ = "noise"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    noise_b_mean = Column(REAL, comment="the background noise in b-arm in electron/pix (mean)")
    noise_b_median = Column(REAL, comment="the background noise in b-arm electron/pix (median)")
    noise_b_sigma = Column(REAL, comment="the background noise in b-arm electron/pix? (sigma)")
    wavelength_ref_b = Column(
        REAL,
        comment="the reference wavelength to measure the sky background noise in b-arm (nm)",
    )
    noise_r_mean = Column(REAL, comment="the background noise in r-arm in electron/pix (mean)")
    noise_r_median = Column(REAL, comment="the background noise in r-arm electron/pix (median)")
    noise_r_sigma = Column(REAL, comment="the background noise in r-arm electron/pix? (sigma)")
    wavelength_ref_r = Column(
        REAL,
        comment="the reference wavelength to measure the sky background noise in r-arm (nm)",
    )
    noise_n_mean = Column(REAL, comment="the background noise in n-arm in electron/pix (mean)")
    noise_n_median = Column(REAL, comment="the background noise in n-arm electron/pix (median)")
    noise_n_sigma = Column(REAL, comment="the background noise in n-arm electron/pix? (sigma)")
    wavelength_ref_n = Column(
        REAL,
        comment="the reference wavelength to measure the sky background noise in n-arm (nm)",
    )
    noise_m_mean = Column(REAL, comment="the background noise in m-arm in electron/pix (mean)")
    noise_m_median = Column(REAL, comment="the background noise in m-arm electron/pix (median)")
    noise_m_sigma = Column(REAL, comment="the background noise in m-arm electron/pix? (sigma)")
    wavelength_ref_m = Column(
        REAL,
        comment="the reference wavelength to measure the sky background noise in m-arm (nm)",
    )

    def __init__(
        self,
        pfs_visit_id,
        noise_b_mean,
        noise_b_median,
        noise_b_sigma,
        wavelength_ref_b,
        noise_r_mean,
        noise_r_median,
        noise_r_sigma,
        wavelength_ref_r,
        noise_n_mean,
        noise_n_median,
        noise_n_sigma,
        wavelength_ref_n,
        noise_m_mean,
        noise_m_median,
        noise_m_sigma,
        wavelength_ref_m,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.noise_b_mean = noise_b_mean
        self.noise_b_median = noise_b_median
        self.noise_b_sigma = noise_b_sigma
        self.wavelength_ref_b = wavelength_ref_b
        self.noise_r_mean = noise_r_mean
        self.noise_r_median = noise_r_median
        self.noise_r_sigma = noise_r_sigma
        self.wavelength_ref_r = wavelength_ref_r
        self.noise_n_mean = noise_n_mean
        self.noise_n_median = noise_n_median
        self.noise_n_sigma = noise_n_sigma
        self.wavelength_ref_n = wavelength_ref_n
        self.noise_m_mean = noise_m_mean
        self.noise_m_median = noise_m_median
        self.noise_m_sigma = noise_m_sigma
        self.wavelength_ref_m = wavelength_ref_m


class moon(Base):
    """Information on the moon for the visit"""

    __tablename__ = "moon"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    moon_phase = Column(REAL, comment="moon phase")
    moon_alt = Column(REAL, comment="moon altitude (deg.)")
    moon_sep = Column(REAL, comment="moon separation to the pointing (deg.)")

    def __init__(
        self,
        pfs_visit_id,
        moon_phase,
        moon_alt,
        moon_sep,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.moon_phase = moon_phase
        self.moon_alt = moon_alt
        self.moon_sep = moon_sep


class sky(Base):
    """Information on the sky background level for the visit"""

    __tablename__ = "sky"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    sky_background_b_mean = Column(
        REAL,
        comment="the mean sky background level in b-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_b_median = Column(
        REAL,
        comment="the median sky background level in b-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_b_sigma = Column(REAL, comment="the sigma of the sky background level in b-arm (counts)")
    wavelength_ref_b = Column(
        REAL,
        comment="the reference wavelength to measure the sky background level in b-arm (nm)",
    )
    sky_background_r_mean = Column(
        REAL,
        comment="the mean sky background level in r-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_r_median = Column(
        REAL,
        comment="the median sky background level in r-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_r_sigma = Column(REAL, comment="the sigma of the sky background level in r-arm (counts)")
    wavelength_ref_r = Column(
        REAL,
        comment="the reference wavelength to measure the sky background level in r-arm (nm)",
    )
    sky_background_n_mean = Column(
        REAL,
        comment="the mean sky background level in n-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_n_median = Column(
        REAL,
        comment="the median sky background level in n-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_n_sigma = Column(REAL, comment="the sigma of the sky background level in n-arm (counts)")
    wavelength_ref_n = Column(
        REAL,
        comment="the reference wavelength to measure the sky background level in n-arm (nm)",
    )
    sky_background_m_mean = Column(
        REAL,
        comment="the mean sky background level in m-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_m_median = Column(
        REAL,
        comment="the median sky background level in m-arm averaged over the FoV/fibers (counts)",
    )
    sky_background_m_sigma = Column(REAL, comment="the sigma of the sky background level in m-arm (counts)")
    wavelength_ref_m = Column(
        REAL,
        comment="the reference wavelength to measure the sky background level in m-arm (nm)",
    )
    agc_background_mean = Column(
        REAL,
        comment="the mean agc image background level averaged over the FoV/fibers (counts)",
    )
    agc_background_median = Column(
        REAL,
        comment="the median agc image background level averaged over the FoV/fibers (counts)",
    )
    agc_background_sigma = Column(REAL, comment="the sigma of the agc image background level (counts)")

    def __init__(
        self,
        pfs_visit_id,
        sky_background_b_mean,
        sky_background_b_median,
        sky_background_b_sigma,
        wavelength_ref_b,
        sky_background_r_mean,
        sky_background_r_median,
        sky_background_r_sigma,
        wavelength_ref_r,
        sky_background_n_mean,
        sky_background_n_median,
        sky_background_n_sigma,
        wavelength_ref_n,
        sky_background_m_mean,
        sky_background_m_median,
        sky_background_m_sigma,
        wavelength_ref_m,
        agc_background_mean,
        agc_background_median,
        agc_background_sigma,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.sky_background_b_mean = sky_background_b_mean
        self.sky_background_b_median = sky_background_b_median
        self.sky_background_b_sigma = sky_background_b_sigma
        self.wavelength_ref_b = wavelength_ref_b
        self.sky_background_r_mean = sky_background_r_mean
        self.sky_background_r_median = sky_background_r_median
        self.sky_background_r_sigma = sky_background_r_sigma
        self.wavelength_ref_r = wavelength_ref_r
        self.sky_background_n_mean = sky_background_n_mean
        self.sky_background_n_median = sky_background_n_median
        self.sky_background_n_sigma = sky_background_n_sigma
        self.wavelength_ref_n = wavelength_ref_n
        self.sky_background_m_mean = sky_background_m_mean
        self.sky_background_m_median = sky_background_m_median
        self.sky_background_m_sigma = sky_background_m_sigma
        self.wavelength_ref_m = wavelength_ref_m
        self.agc_background_mean = agc_background_mean
        self.agc_background_median = agc_background_median
        self.agc_background_sigma = agc_background_sigma


class telescope(Base):
    """Information on the telescope status"""

    __tablename__ = "telescope"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    azimuth = Column(REAL, comment="the average telescope azimuth during the exposure (deg.)")
    altitude = Column(REAL, comment="the average telescope altitude during the exposure (deg.)")
    airmass = Column(REAL, comment="the average airmass during the exposure (deg.)")

    def __init__(
        self,
        pfs_visit_id,
        azimuth,
        altitude,
        airmass,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.azimuth = azimuth
        self.altitude = altitude
        self.airmass = airmass


class cobra_convergence(Base):
    """Quality of the cobra convergence for the visit"""

    __tablename__ = "cobra_convergence"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    number_converged = Column(Integer, comment="the number of converged targets within the threshold")
    residual_mean = Column(REAL, comment="the mean residual of fiber configuration (um)")
    residual_median = Column(REAL, comment="the median residual of fiber configuration (um)")
    residual_sigma = Column(REAL, comment="the sigma of the residual of fiber configuration (um)")

    def __init__(
        self,
        pfs_visit_id,
        number_converged,
        residual_mean,
        residual_median,
        residual_sigma,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.number_converged = number_converged
        self.residual_mean = residual_mean
        self.residual_median = residual_median
        self.residual_sigma = residual_sigma


class guide_offset(Base):
    """Statistics of the AGC guide errors during the exposure"""

    __tablename__ = "guide_offset"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    number_guide_stars = Column(Integer, comment="the number of guide targets used")
    offset_mean = Column(REAL, comment="the mean guide offset during the exposure (arcsec)")
    offset_median = Column(REAL, comment="the median guide offset during the exposure (arcsec)")
    offset_sigma = Column(REAL, comment="the sigma of the guide offset during the exposure (arcsec)")

    def __init__(
        self,
        pfs_visit_id,
        number_guide_stars,
        offset_mean,
        offset_median,
        offset_sigma,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.number_guide_stars = number_guide_stars
        self.offset_mean = offset_mean
        self.offset_median = offset_median
        self.offset_sigma = offset_sigma


class exposure_time(Base):
    """Information on the exposure_time for the visit"""

    __tablename__ = "exposure_time"

    pfs_visit_id = Column(
        Integer,
        ForeignKey("pfs_visit.pfs_visit_id"),
        primary_key=True,
        unique=True,
        autoincrement=False,
    )
    nominal_exposure_time = Column(REAL, comment="the nominal exposure time (sec.)")
    effective_exposure_time_b = Column(
        REAL,
        comment="the effective exposure time inferred with the observed condition in b-arm (sec.)",
    )
    effective_exposure_time_r = Column(
        REAL,
        comment="the effective exposure time inferred with the observed condition in r-arm (sec.)",
    )
    effective_exposure_time_n = Column(
        REAL,
        comment="the effective exposure time inferred with the observed condition in n-arm (sec.)",
    )
    effective_exposure_time_m = Column(
        REAL,
        comment="the effective exposure time inferred with the observed condition in m-arm (sec.)",
    )

    def __init__(
        self,
        pfs_visit_id,
        nominal_exposure_time,
        effective_exposure_time_b,
        effective_exposure_time_r,
        effective_exposure_time_n,
        effective_exposure_time_m,
    ):
        self.pfs_visit_id = pfs_visit_id
        self.nominal_exposure_time = nominal_exposure_time
        self.effective_exposure_time_b = effective_exposure_time_b
        self.effective_exposure_time_r = effective_exposure_time_r
        self.effective_exposure_time_n = effective_exposure_time_n
        self.effective_exposure_time_m = effective_exposure_time_m


## DRP2D QA tables ##


class calibs(Base):
    """Information on the calibration"""

    __tablename__ = "calibs"

    calib_id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment="CLAIBs ID")
    calib_name = Column(String, comment="the name of CALIB (e.g. CALIB-2024-07-v1)")
    calib_description = Column(String, comment="the description of CALIB")
    drp_version = Column(String, comment="DRP2D version (e.g., w.2023.20)")
    generated_at = Column(DateTime, comment="the type of calibration")

    def __init__(
        self,
        calib_id,
        calib_name,
        calib_description,
        drp_version,
        generated_at,
    ):
        self.calib_id = calib_id
        self.calib_name = calib_name
        self.calib_description = calib_description
        self.drp_version = drp_version
        self.generated_at = generated_at


class calibs_qa(Base):
    """Information on the calibration QA"""

    __tablename__ = "calibs_qa"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    calib_id = Column(Integer, ForeignKey("calibs.calib_id"), comment="CLAIBs ID")
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    bias_qa = Column(REAL, comment="QA for bias")
    dark_qa = Column(REAL, comment="QA for dark")
    detectormap_qa = Column(REAL, comment="QA for detectorMap")
    fiberprofiles_qa = Column(REAL, comment="QA for fiberProfiles")
    fibernorms_qa = Column(REAL, comment="QA for fiberNorms")
    processed_at = Column(DateTime, comment="datetime of the QA processing")
    status = Column(Integer, comment="QA processing status")

    def __init__(
        self,
        calib_id,
        drp_qa_version,
        bias_qa,
        dark_qa,
        detectormap_qa,
        fiberprofiles_qa,
        fibernorms_qa,
        processed_at,
        status,
    ):
        self.calib_id = calib_id
        self.drp_qa_version = drp_qa_version
        self.bias_qa = bias_qa
        self.dark_qa = dark_qa
        self.detectormap_qa = detectormap_qa
        self.fiberprofiles_qa = fiberprofiles_qa
        self.fibernorms_qa = fibernorms_qa
        self.processed_at = processed_at
        self.status = status


class calibs_qa_detector(Base):
    """Information on the calibration QA"""

    __tablename__ = "calibs_qa_detector"
    __table_args__ = (UniqueConstraint("qa_id", "arm", "spectrograph"), {})

    qa_id = Column(Integer, ForeignKey("calibs_qa.qa_id"), primary_key=True, comment="CLAIBs QA ID")
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, primary_key=True, comment="spectrograph (1/2/3/4)")
    bias_qa = Column(REAL, comment="QA for bias")
    dark_qa = Column(REAL, comment="QA for dark")
    detectormap_qa = Column(REAL, comment="QA for detectorMap")
    fiberprofiles_qa = Column(REAL, comment="QA for fiberProfiles")
    fibernorms_qa = Column(REAL, comment="QA for fiberNorms")

    def __init__(
        self,
        qa_id,
        spectrograph,
        arm,
        bias_qa,
        dark_qa,
        detectormap_qa,
        fiberprofiles_qa,
        fibernorms_qa,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.bias_qa = bias_qa
        self.dark_qa = dark_qa
        self.detectormap_qa = detectormap_qa
        self.fiberprofiles_qa = fiberprofiles_qa
        self.fibernorms_qa = fibernorms_qa


class drp2d_processing(Base):
    """Information of the 2D DRP processing"""

    __tablename__ = "drp2d_processing"

    processing_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    rerun = Column(String, comment="rerun name of the processing")
    description = Column(String, comment="description of the processing")
    calib_id = Column(Integer, ForeignKey("calibs.calib_id"), comment="CLAIBs ID")
    drp_version = Column(String, comment="DRP2D version (e.g., w.2023.20)")
    processed_at = Column(DateTime, comment="datetime of the processing")
    status = Column(Integer, comment="Processing status")

    def __init__(
        self,
        rerun,
        description,
        drp_version,
        processed_at,
        status,
    ):
        self.rerun = rerun
        self.description = description
        self.drp_version = drp_version
        self.processed_at = processed_at
        self.status = status


class drp2d_processing_qa(Base):
    """Information on the 2D DRP processing QA results"""

    __tablename__ = "drp2d_processing_qa"

    qa_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
        primary_key=True,
        unique=False,
        autoincrement=False,
    )
    pfs_visit_id = Column(Integer)
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    detectormap_qa_result = Column(REAL, comment="TBD")
    extraction_qa_result = Column(REAL, comment="TBD")
    sky_subtraction_qa_result = Column(REAL, comment="TBD")
    flux_calibration_qa_result = Column(REAL, comment="TBD")

    def __init__(
        self,
        qa_id,
        processing_id,
        pfs_visit_id,
        drp_qa_version,
        detectormap_qa_result,
        extraction_qa_result,
        sky_subtraction_qa_result,
        flux_calibration_qa_result,
    ):
        self.qa_id = qa_id
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.drp_qa_version = drp_qa_version
        self.detectormap_qa_result = detectormap_qa_result
        self.extraction_qa_result = extraction_qa_result
        self.sky_subtraction_qa_result = sky_subtraction_qa_result
        self.flux_calibration_qa_result = flux_calibration_qa_result


class detectormap_qa(Base):
    """Quality of the detectorMap for the visit"""

    __tablename__ = "detectormap_qa"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=False,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    processed_at = Column(DateTime, comment="datetime of the QA processing")
    status = Column(Integer, comment="QA processing status")
    residual_wavelength_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_wavelength_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_wavelength_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")
    residual_trace_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_trace_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_trace_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")

    def __init__(
        self,
        processing_id,
        pfs_visit_id,
        drp_qa_version,
        processed_at,
        status,
        residual_wavelength_mean,
        residual_wavelength_median,
        residual_wavelength_sigma,
        residual_trace_mean,
        residual_trace_median,
        residual_trace_sigma,
    ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.drp_qa_version = drp_qa_version
        self.processed_at = processed_at
        self.status = status
        self.residual_wavelength_mean = residual_wavelength_mean
        self.residual_wavelength_median = residual_wavelength_median
        self.residual_wavelength_sigma = residual_wavelength_sigma
        self.residual_trace_mean = residual_trace_mean
        self.residual_trace_median = residual_trace_median
        self.residual_trace_sigma = residual_trace_sigma


class detectormap_qa_detector(Base):
    """Quality of the detectorMap"""

    __tablename__ = "detectormap_qa_detector"
    __table_args__ = (UniqueConstraint("qa_id", "arm", "spectrograph"), {})

    qa_id = Column(
        Integer,
        ForeignKey("detectormap_qa.qa_id"),
        primary_key=True,
    )
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, primary_key=True, comment="spectrograph (1/2/3/4)")
    residual_wavelength_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_wavelength_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_wavelength_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")
    residual_trace_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_trace_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_trace_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")

    def __init__(
        self,
        qa_id,
        arm,
        spectrograph,
        residual_wavelength_mean,
        residual_wavelength_median,
        residual_wavelength_sigma,
        residual_trace_mean,
        residual_trace_median,
        residual_trace_sigma,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.residual_wavelength_mean = residual_wavelength_mean
        self.residual_wavelength_median = residual_wavelength_median
        self.residual_wavelength_sigma = residual_wavelength_sigma
        self.residual_trace_mean = residual_trace_mean
        self.residual_trace_median = residual_trace_median
        self.residual_trace_sigma = residual_trace_sigma


class detectormap_qa_fiber(Base):
    """Quality of the detectorMap"""

    __tablename__ = "detectormap_qa_fiber"
    __table_args__ = (UniqueConstraint("qa_id", "fiber_id", "arm"), {})

    qa_id = Column(
        Integer,
        ForeignKey("detectormap_qa.qa_id"),
        primary_key=True,
    )
    fiber_id = Column(
        Integer,
        primary_key=True,
    )
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, comment="spectrograph (1/2/3/4)")
    residual_wavelength_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_wavelength_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_wavelength_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")
    residual_trace_mean = Column(REAL, comment="the mean wavelength residual averaged over fibers (nm)")
    residual_trace_median = Column(REAL, comment="the median wavelength residual averaged over fibers (nm)")
    residual_trace_sigma = Column(REAL, comment="the sigma of the wavelength residual averaged over fibers (nm)")

    def __init__(
        self,
        qa_id,
        fiber_id,
        arm,
        spectrograph,
        residual_wavelength_mean,
        residual_wavelength_median,
        residual_wavelength_sigma,
        residual_trace_mean,
        residual_trace_median,
        residual_trace_sigma,
    ):
        self.qa_id = qa_id
        self.fiber_id = fiber_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.residual_wavelength_mean = residual_wavelength_mean
        self.residual_wavelength_median = residual_wavelength_median
        self.residual_wavelength_sigma = residual_wavelength_sigma
        self.residual_trace_mean = residual_trace_mean
        self.residual_trace_median = residual_trace_median
        self.residual_trace_sigma = residual_trace_sigma


class extraction_qa(Base):
    """Quality of the spectral extraction for the visit"""

    __tablename__ = "extraction_qa"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=False,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    processed_at = Column(DateTime, comment="datetime of the QA processing")
    status = Column(Integer, comment="QA processing status")
    number_of_extracted_fibers = Column(Integer, comment="the number of the number of extracted fibers")
    residual_chi_mean = Column(
        REAL,
        comment="the mean sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_median = Column(
        REAL,
        comment="the median sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_sigma = Column(REAL, comment="the sigma of the sky subtraction residual in chi (counts)")

    def __init__(
        self,
        processing_id,
        pfs_visit_id,
        drp_qa_version,
        processed_at,
        status,
        number_of_extracted_fibers,
        residual_chi_mean,
        residual_chi_median,
        residual_chi_sigma,
    ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.drp_qa_version = drp_qa_version
        self.processed_at = processed_at
        self.status = status
        self.number_of_extracted_fibers = number_of_extracted_fibers
        self.residual_chi_mean = residual_chi_mean
        self.residual_chi_median = residual_chi_median
        self.residual_chi_sigma = residual_chi_sigma


class extraction_qa_detector(Base):
    """Quality of the spectral extraction for the visit per detector"""

    __tablename__ = "extraction_qa_detector"
    __table_args__ = (UniqueConstraint("qa_id", "arm", "spectrograph"), {})

    qa_id = Column(
        Integer,
        ForeignKey("extraction_qa.qa_id"),
        primary_key=True,
    )
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, primary_key=True, comment="spectrograph (1/2/3/4)")
    number_of_extracted_fibers = Column(Integer, comment="the number of extracted fibers")
    residual_chi_mean = Column(
        REAL,
        comment="the mean sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_median = Column(
        REAL,
        comment="the median sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_sigma = Column(REAL, comment="the sigma of the sky subtraction residual in chi (counts)")

    def __init__(
        self,
        qa_id,
        arm,
        spectrograph,
        number_of_sky_fibers,
        residual_chi_mean,
        residual_chi_median,
        residual_chi_sigma,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.number_of_sky_fibers = number_of_sky_fibers
        self.residual_chi_mean = residual_chi_mean
        self.residual_chi_median = residual_chi_median
        self.residual_chi_sigma = residual_chi_sigma


class sky_subtraction_qa(Base):
    """Quality of the sky subtraction for the visit"""

    __tablename__ = "sky_subtraction_qa"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=False,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    processed_at = Column(DateTime, comment="datetime of the QA processing")
    status = Column(Integer, comment="QA processing status")
    number_of_sky_fibers = Column(Integer, comment="the number of sky fibers to make the sky model")
    residual_chi_mean = Column(
        REAL,
        comment="the mean sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_median = Column(
        REAL,
        comment="the median sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_sigma = Column(REAL, comment="the sigma of the sky subtraction residual in chi (counts)")

    def __init__(
        self,
        processing_id,
        pfs_visit_id,
        drp_qa_version,
        processed_at,
        status,
        number_of_sky_fibers,
        residual_chi_mean,
        residual_chi_median,
        residual_chi_sigma,
    ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.drp_qa_version = drp_qa_version
        self.processed_at = processed_at
        self.status = status
        self.number_of_sky_fibers = number_of_sky_fibers
        self.residual_chi_mean = residual_chi_mean
        self.residual_chi_median = residual_chi_median
        self.residual_chi_sigma = residual_chi_sigma


class sky_subtraction_qa_detector(Base):
    """Quality of the sky subtraction for the visit per detector"""

    __tablename__ = "sky_subtraction_qa_detector"
    __table_args__ = (UniqueConstraint("qa_id", "arm", "spectrograph"), {})

    qa_id = Column(
        Integer,
        ForeignKey("sky_subtraction_qa.qa_id"),
        primary_key=True,
    )
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, primary_key=True, comment="spectrograph (1/2/3/4)")
    number_of_sky_fibers = Column(Integer, comment="the number of sky fibers to make the sky model")
    residual_chi_mean = Column(
        REAL,
        comment="the mean sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_median = Column(
        REAL,
        comment="the median sky subtraction residual in chi averaged over FoV (counts)",
    )
    residual_chi_sigma = Column(REAL, comment="the sigma of the sky subtraction residual in chi (counts)")

    def __init__(
        self,
        qa_id,
        arm,
        spectrograph,
        number_of_sky_fibers,
        residual_chi_mean,
        residual_chi_median,
        residual_chi_sigma,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.number_of_sky_fibers = number_of_sky_fibers
        self.residual_chi_mean = residual_chi_mean
        self.residual_chi_median = residual_chi_median
        self.residual_chi_sigma = residual_chi_sigma


class flux_calibration_qa(Base):
    """Quality of the flux calibration for the visit"""

    __tablename__ = "flux_calibration_qa"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=False,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    drp_qa_version = Column(String, comment="drp_qa version (e.g., w.2024.33)")
    processed_at = Column(DateTime, comment="datetime of the QA processing")
    status = Column(Integer, comment="QA processing status")
    number_of_flux_standards = Column(Integer, comment="the number of flux standard stars to calculate the vector")
    tbd = Column(REAL, comment="TBD")

    def __init__(
        self,
        processing_id,
        pfs_visit_id,
        drp_qa_version,
        processed_at,
        status,
        number_of_flux_standards,
        tbd,
    ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.drp_qa_version = drp_qa_version
        self.processed_at = processed_at
        self.status = status
        self.number_of_flux_standards = number_of_flux_standards
        self.tbd = tbd


class flux_calibration_qa_detector(Base):
    """Quality of the flux calibration for the visit"""

    __tablename__ = "flux_calibration_qa_detector"
    __table_args__ = (UniqueConstraint("qa_id", "arm", "spectrograph"), {})

    qa_id = Column(
        Integer,
        ForeignKey("flux_calibration_qa.qa_id"),
        primary_key=True,
    )
    arm = Column(String(1), primary_key=True, comment="arm (b/r/n/m)")
    spectrograph = Column(Integer, primary_key=True, comment="spectrograph (1/2/3/4)")
    number_of_flux_standards = Column(Integer, comment="the number of flux standard stars to calculate the vector")
    tbd = Column(REAL, comment="TBD")

    def __init__(
        self,
        qa_id,
        arm,
        spectrograph,
        number_of_flux_standards,
        tbd,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.spectrograph = spectrograph
        self.number_of_flux_standards = number_of_flux_standards
        self.tbd = tbd


class cosmic_rays(Base):
    """Quality of the cosmic rays detection for the visit"""

    __tablename__ = "cosmic_rays"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    tbd = Column(REAL, comment="TBD")

    def __init__(
        self,
        qa_id,
        processing_id,
        pfs_visit_id,
        tbd,
    ):
        self.qa_id = qa_id
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.tbd = tbd


class mask(Base):
    """Information on the bit masks in the reduced products"""

    __tablename__ = "mask"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    number_of_pix_in_each_bit = Column(Integer, comment="TBD")

    def __init__(
        self,
        qa_id,
        arm,
        number_of_pix_in_each_bit,
    ):
        self.qa_id = qa_id
        self.arm = arm
        self.number_of_pix_in_each_bit = number_of_pix_in_each_bit


class h4_persistence(Base):
    """Quality of the H4RG persistence correction for the visit"""

    __tablename__ = "h4_persistence"

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    tbd = Column(REAL, comment="TBD")

    def __init__(
        self,
        qa_id,
        spectrograph,
        tbd,
    ):
        self.qa_id = qa_id
        self.spectrograph = spectrograph
        self.tbd = tbd


class dichroic_continuity(Base):
    """Check the dichroic continuity after merging the arms"""

    __tablename__ = "dichroic_continuity"
    __table_args__ = (UniqueConstraint("qa_id"), {})

    qa_id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    processing_id = Column(
        Integer,
        ForeignKey("drp2d_processing.processing_id"),
    )
    pfs_visit_id = Column(Integer, comment="pfs_visit_id")
    br_continuity = Column(REAL, comment="TBD")
    rn_continuity = Column(REAL, comment="TBD")

    def __init__(
        self,
        qa_id,
        processing_id,
        pfs_visit_id,
        br_continuity,
        rn_continuity,
    ):
        self.qa_id = qa_id
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.br_continuity = br_continuity
        self.rn_continuity = rn_continuity


## DRP1D QA tables ##


class drp1d_processing(Base):
    """Information of the 1D DRP processing"""

    __tablename__ = "drp1d_processing"

    processing_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    rerun = Column(String, comment="rerun name of the processing")
    description = Column(String, comment="description of the processing")
    drp_version = Column(String, comment="DRP1D version (e.g., 0.40.0)")
    processed_at = Column(DateTime, comment="datetime of the processing")
    status = Column(Integer, comment="Processing status")

    def __init__(
        self,
        processing_id,
        rerun,
        description,
        drp_version,
        processed_at,
        status,
    ):
        self.processing_id = processing_id
        self.rerun = rerun
        self.description = description
        self.drp_version = drp_version
        self.processed_at = processed_at
        self.status = status


class drp1d_processing_qa(Base):
    """Information on the 1D DRP processing results"""

    __tablename__ = "drp1d_processing_qa"

    qa_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    processing_id = Column(
        Integer,
        ForeignKey("drp1d_processing.processing_id"),
        primary_key=True,
        unique=False,
        autoincrement=False,
    )
    pfs_visit_id = Column(Integer)
    qa_version = Column(String, comment="QA code version (e.g., xxxxx)")
    qa_type = Column(String, comment="the type of QA processing")
    processed_at = Column(DateTime, comment="datetime of the processing")

    def __init__(
        self,
        qa_id,
        processing_id,
        pfs_visit_id,
        qa_version,
        qa_type,
        processed_at,
    ):
        self.qa_id = qa_id
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.qa_version = qa_version
        self.qa_type = qa_type
        self.processed_at = processed_at


class redshift_measurement(Base):
    """Quality of 1D redshift measurements"""

    __tablename__ = "redshift_measurement"

    qa_id = Column(
        Integer,
        ForeignKey("drp1d_processing_qa.qa_id"),
        primary_key=True,
        unique=False,
        autoincrement=False,
    )
    number_of_galaxies = Column(Integer, comment="the number of galaxies classified")
    chisq_mean = Column(REAL, comment="the mean chi^2 in the fitting")
    chisq_median = Column(REAL, comment="the median chi^2 in the fitting")
    chisq_sigma = Column(REAL, comment="the sigma of the chi^2 in the fitting")

    def __init__(
        self,
        qa_id,
        number_of_galaxies,
        chisq_mean,
        chisq_median,
        chisq_sigma,
    ):
        self.qa_id = qa_id
        self.number_of_galaxies = number_of_galaxies
        self.chisq_mean = chisq_mean
        self.chisq_median = chisq_median
        self.chisq_sigma = chisq_sigma


def make_database(dbinfo):
    """
    dbinfo is something like this: postgresql://xxxxx:yyyyy@zzz.zzz.zzz.zz/dbname
    """
    # engine = create_engine('sqlite:///:memory:', echo=True)
    # engine = create_engine('sqlite:///pfs_proto.sqlite', echo=False)
    engine = create_engine(dbinfo)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session()


if __name__ == "__main__":
    import sys

    dbinfo = sys.argv[1]
    print(dbinfo)
    make_database(dbinfo)
