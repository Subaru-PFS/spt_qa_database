from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, DateTime, Boolean, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint

Base = declarative_base()


class test(Base):
    __tablename__ = 'test'

    test_id = Column(Integer, primary_key=True,
                     unique=True, autoincrement=True)
    test_val1 = Column(Integer, comment='test_val1')
    test_val2 = Column(REAL, comment='test_val2')
    test_val3 = Column(String, comment='test_val3')
    test_val4 = Column(DateTime, comment='test_val4')

    def __init__(self, test_val1, test_val2, test_val3, test_val4):
        self.test_val1 = test_val1
        self.test_val2 = test_val2
        self.test_val3 = test_val3
        self.test_val4 = test_val4


class pfs_visit(Base):
    '''Tracks the Gen2 visit identifier.
    This is the fundamental identifier for all instrument exposures (MCS, AGC, SPS)
    <<<<< copied from opDB models.py >>>>>
    '''
    __tablename__ = 'pfs_visit'

    pfs_visit_id = Column(Integer, primary_key=True,
                          unique=True, autoincrement=False)
    pfs_visit_description = Column(String)
    pfs_design_id = Column(BigInteger)
    issued_at = Column(DateTime, comment='Issued time [YYYY-MM-DDThh:mm:ss]')

    def __init__(self, pfs_visit_id, pfs_visit_description, pfs_design_id, issued_at):
        self.pfs_visit_id = pfs_visit_id
        self.pfs_visit_description = pfs_visit_description
        self.pfs_design_id = pfs_design_id
        self.issued_at = issued_at


class seeing(Base):
    '''Statistics of seeing during a single SpS exposure
    '''
    __tablename__ = 'seeing'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    seeing_mean = Column(REAL, comment='seeing FWHM mean (arcsec.)')
    seeing_median = Column(REAL, comment='seeing FWHM median (arcsec.)')
    seeing_sigma = Column(REAL, comment='seeing FWHM sigma (arcsec.)')
    wavelength_ref = Column(REAL,
                            comment='the reference wavelength to measure the seeing (nm)')

    def __init__(self,
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
    '''Statistics of seeing during a single AGC exposure
    '''
    __tablename__ = 'seeing_agc_exposure'
    __table_args__ = (UniqueConstraint('pfs_visit_id', 'agc_exposure_id'), {})

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, autoincrement=False)
    agc_exposure_id = Column(Integer, autoincrement=False)
    seeing_mean = Column(REAL, comment='seeing FWHM mean (arcsec.)')
    seeing_median = Column(REAL, comment='seeing FWHM median (arcsec.)')
    seeing_sigma = Column(REAL, comment='seeing FWHM sigma (arcsec.)')
    wavelength_ref = Column(
        REAL, comment='the reference wavelength to measure the seeing (nm)')
    taken_at = Column(
        DateTime, comment='The time at which the exposure was taken [YYYY-MM-DDThh-mm-sss]')

    def __init__(self,
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
    '''Statistics of transparency during a single SpS exposure
    '''
    __tablename__ = 'transparency'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    transparency_mean = Column(REAL, comment='transparency mean')
    transparency_median = Column(REAL, comment='transparency median')
    transparency_sigma = Column(REAL, comment='transparency sigma')
    wavelength_ref = Column(REAL,
                            comment='the reference wavelength to measure the transparency (nm)')

    def __init__(self,
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
    '''Statistics of transparency during a single AGC exposure
    '''
    __tablename__ = 'transparency_agc_exposure'
    __table_args__ = (UniqueConstraint('pfs_visit_id', 'agc_exposure_id'), {})

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, autoincrement=False)
    agc_exposure_id = Column(Integer,
                             primary_key=True, autoincrement=False)
    transparency_mean = Column(REAL, comment='transparency mean')
    transparency_median = Column(REAL, comment='transparency median')
    transparency_sigma = Column(REAL, comment='transparency sigma')
    wavelength_ref = Column(REAL,
                            comment='the reference wavelength to measure the transparency (nm)')
    taken_at = Column(
        DateTime, comment='The time at which the exposure was taken [YYYY-MM-DDThh-mm-sss]')

    def __init__(self,
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
    '''Total throughput for the visit
    '''
    __tablename__ = 'throughput'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    throughput_b_mean = Column(
        REAL, comment='the total throughput in b-arm (mean)')
    throughput_b_median = Column(
        REAL, comment='the total throughput in b-arm (median)')
    throughput_b_sigma = Column(
        REAL, comment='the total throughput in b-arm (sigma)')
    wavelength_ref_b = Column(
        REAL, comment='the reference wavelength to measure the total throughput (nm)')
    throughput_r_mean = Column(
        REAL, comment='the total throughput in r-arm (mean)')
    throughput_r_median = Column(
        REAL, comment='the total throughput in r-arm (median)')
    throughput_r_sigma = Column(
        REAL, comment='the total throughput in r-arm (sigma)')
    wavelength_ref_r = Column(
        REAL, comment='the reference wavelength to measure the total throughput (nm)')
    throughput_n_mean = Column(
        REAL, comment='the total throughput in n-arm (mean)')
    throughput_n_median = Column(
        REAL, comment='the total throughput in n-arm (median)')
    throughput_n_sigma = Column(
        REAL, comment='the total throughput in n-arm (sigma)')
    wavelength_ref_n = Column(
        REAL, comment='the reference wavelength to measure the total throughput (nm)')
    throughput_m_mean = Column(
        REAL, comment='the total throughput in m-arm (mean)')
    throughput_m_median = Column(
        REAL, comment='the total throughput in m-arm (median)')
    throughput_m_sigma = Column(
        REAL, comment='the total throughput in m-arm (sigma)')
    wavelength_ref_m = Column(
        REAL, comment='the reference wavelength to measure the total throughput (nm)')

    def __init__(self,
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
    '''Background noise level for the visit
    '''
    __tablename__ = 'noise'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    noise_b_mean = Column(
        REAL, comment='the background noise in b-arm in electron/pix (mean)')
    noise_b_median = Column(
        REAL, comment='the background noise in b-arm electron/pix (median)')
    noise_b_sigma = Column(
        REAL, comment='the background noise in b-arm electron/pix? (sigma)')
    wavelength_ref_b = Column(
        REAL, comment='the reference wavelength to measure the sky background noise in b-arm (nm)')
    noise_r_mean = Column(
        REAL, comment='the background noise in r-arm in electron/pix (mean)')
    noise_r_median = Column(
        REAL, comment='the background noise in r-arm electron/pix (median)')
    noise_r_sigma = Column(
        REAL, comment='the background noise in r-arm electron/pix? (sigma)')
    wavelength_ref_r = Column(
        REAL, comment='the reference wavelength to measure the sky background noise in r-arm (nm)')
    noise_n_mean = Column(
        REAL, comment='the background noise in n-arm in electron/pix (mean)')
    noise_n_median = Column(
        REAL, comment='the background noise in n-arm electron/pix (median)')
    noise_n_sigma = Column(
        REAL, comment='the background noise in n-arm electron/pix? (sigma)')
    wavelength_ref_n = Column(
        REAL, comment='the reference wavelength to measure the sky background noise in n-arm (nm)')
    noise_m_mean = Column(
        REAL, comment='the background noise in m-arm in electron/pix (mean)')
    noise_m_median = Column(
        REAL, comment='the background noise in m-arm electron/pix (median)')
    noise_m_sigma = Column(
        REAL, comment='the background noise in m-arm electron/pix? (sigma)')
    wavelength_ref_m = Column(
        REAL, comment='the reference wavelength to measure the sky background noise in m-arm (nm)')

    def __init__(self,
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
    '''Information on the moon for the visit
    '''
    __tablename__ = 'moon'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    moon_phase = Column(REAL, comment='moon phase')
    moon_alt = Column(REAL, comment='moon altitude (deg.)')
    moon_sep = Column(REAL, comment='moon separation to the pointing (deg.)')

    def __init__(self,
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
    '''Information on the sky background level for the visit
    '''
    __tablename__ = 'sky'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    sky_background_b_mean = Column(
        REAL, comment='the mean sky background level in b-arm averaged over the FoV/fibers (counts)')
    sky_background_b_median = Column(
        REAL, comment='the median sky background level in b-arm averaged over the FoV/fibers (counts)')
    sky_background_b_sigma = Column(
        REAL, comment='the sigma of the sky background level in b-arm (counts)')
    wavelength_ref_b = Column(
        REAL, comment='the reference wavelength to measure the sky background level in b-arm (nm)')
    sky_background_r_mean = Column(
        REAL, comment='the mean sky background level in r-arm averaged over the FoV/fibers (counts)')
    sky_background_r_median = Column(
        REAL, comment='the median sky background level in r-arm averaged over the FoV/fibers (counts)')
    sky_background_r_sigma = Column(
        REAL, comment='the sigma of the sky background level in r-arm (counts)')
    wavelength_ref_r = Column(
        REAL, comment='the reference wavelength to measure the sky background level in r-arm (nm)')
    sky_background_n_mean = Column(
        REAL, comment='the mean sky background level in n-arm averaged over the FoV/fibers (counts)')
    sky_background_n_median = Column(
        REAL, comment='the median sky background level in n-arm averaged over the FoV/fibers (counts)')
    sky_background_n_sigma = Column(
        REAL, comment='the sigma of the sky background level in n-arm (counts)')
    wavelength_ref_n = Column(
        REAL, comment='the reference wavelength to measure the sky background level in n-arm (nm)')
    sky_background_m_mean = Column(
        REAL, comment='the mean sky background level in m-arm averaged over the FoV/fibers (counts)')
    sky_background_m_median = Column(
        REAL, comment='the median sky background level in m-arm averaged over the FoV/fibers (counts)')
    sky_background_m_sigma = Column(
        REAL, comment='the sigma of the sky background level in m-arm (counts)')
    wavelength_ref_m = Column(
        REAL, comment='the reference wavelength to measure the sky background level in m-arm (nm)')
    agc_background_mean = Column(
        REAL, comment='the mean agc image background level averaged over the FoV/fibers (counts)')
    agc_background_median = Column(
        REAL, comment='the median agc image background level averaged over the FoV/fibers (counts)')
    agc_background_sigma = Column(
        REAL, comment='the sigma of the agc image background level (counts)')

    def __init__(self,
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
    '''Information on the telescope status
    '''
    __tablename__ = 'telescope'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    azimuth = Column(
        REAL, comment='the average telescope azimuth during the exposure (deg.)')
    altitude = Column(
        REAL, comment='the average telescope altitude during the exposure (deg.)')
    airmass = Column(
        REAL, comment='the average airmass during the exposure')

    def __init__(self,
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
    '''Quality of the cobra convergence for the visit
    '''
    __tablename__ = 'cobra_convergence'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    number_converged = Column(
        Integer, comment='the number of converged targets within the threshold')
    residual_mean = Column(REAL,
                           comment='the mean residual of fiber configuration (um)')
    residual_median = Column(REAL,
                             comment='the median residual of fiber configuration (um)')
    residual_sigma = Column(REAL,
                            comment='the sigma of the residual of fiber configuration (um)')

    def __init__(self,
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
    '''Statistics of the AGC guide errors during the exposure
    '''
    __tablename__ = 'guide_offset'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    number_guide_stars = Column(
        Integer, comment='the number of guide targets used')
    offset_mean = Column(REAL,
                         comment='the mean guide offset during the exposure (arcsec)')
    offset_median = Column(REAL,
                           comment='the median guide offset during the exposure (arcsec)')
    offset_sigma = Column(REAL,
                          comment='the sigma of the guide offset during the exposure (arcsec)')

    def __init__(self,
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
    '''Information on the exposure_time for the visit
    '''
    __tablename__ = 'exposure_time'

    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True, unique=True, autoincrement=False)
    nominal_exposure_time = Column(
        REAL, comment='the nominal exposure time (sec.)')
    effective_exposure_time_b = Column(REAL,
                                       comment='the effective exposure time inferred with the observed condition in b-arm (sec.)')
    effective_exposure_time_r = Column(REAL,
                                       comment='the effective exposure time inferred with the observed condition in r-arm (sec.)')
    effective_exposure_time_n = Column(REAL,
                                       comment='the effective exposure time inferred with the observed condition in n-arm (sec.)')
    effective_exposure_time_m = Column(REAL,
                                       comment='the effective exposure time inferred with the observed condition in m-arm (sec.)')

    def __init__(self,
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


class onsite_processing_status(Base):
    '''Status of the DRP on-site processing
    '''
    __tablename__ = 'onsite_processing_status'

    pfs_visit_id = Column(Integer,
                          primary_key=True,
                          unique=True,
                          autoincrement=False,
                          comment='PFS visit ID')
    status = Column(Integer,
                    comment='Status of processing (0=in progress, 1=completed successfully, 2=completed but failed)')
    started_at = Column(DateTime,
                        comment='datetime of the processing start')
    updated_at = Column(DateTime,
                        comment='datetime of the status update')

    def __init__(self,
                 pfs_visit_id,
                 status,
                 started_at,
                 updated_at,
                 ):
        self.pfs_visit_id = pfs_visit_id
        self.status = status
        self.started_at = started_at
        self.updated_at = updated_at

## DRP QA tables ##


class data_processing_pipe2d(Base):
    '''Information of the pipeline processing
    '''
    __tablename__ = 'data_processing_pipe2d'

    processing_id = Column(Integer,
                           primary_key=True,
                           autoincrement=True,
                           )
    collection_name = Column(String,
                             comment='pipe2d collection name (e.g. PFS/calib/pipe2d-1842/run28/verifyCalib.calibs.20260520a)')
    run_name = Column(String,
                      comment='pipe2d RUN name (e.g. 20260521T061122Z)')
    pipe2d_version = Column(String,
                            comment='pipe2d version (e.g., w.2026.20)')
    drp_qa_version = Column(String,
                            comment='drp_qa version (e.g., w.2026.20)')

    def __init__(self,
                 collection_name,
                 run_name,
                 pipe2d_version,
                 drp_qa_version,
                 ):
        self.collection_name = collection_name
        self.run_name = run_name
        self.pipe2d_version = pipe2d_version
        self.drp_qa_version = drp_qa_version


class data_qa(Base):
    '''Information of the pipeline processing
    '''
    __tablename__ = 'data_qa'

    run_id = Column(Integer,
                    primary_key=True,
                    unique=True,
                    autoincrement=True)
    pfs_visit_id = Column(Integer, ForeignKey('pfs_visit.pfs_visit_id'))
    pipe2d_version = Column(String,
                            comment='pipe2d version (e.g., w.2025.20)')
    drp_qa_version = Column(String,
                            comment='drp_qa version (e.g., w.2025.20)')
    process_type = Column(String,
                          comment='process_type')
    process_datetime_start = Column(DateTime,
                                    comment='datetime of the processing run start')
    process_datetime_end = Column(DateTime,
                                  comment='datetime of the processing run end')

    def __init__(self,
                 pfs_visit_id,
                 pipe2d_version,
                 drp_qa_version,
                 process_type,
                 process_datetime_start,
                 process_datetime_end,
                 ):
        self.pfs_visit_id = pfs_visit_id
        self.pipe2d_version = pipe2d_version
        self.drp_qa_version = drp_qa_version
        self.process_type = process_type
        self.process_datetime_start = process_datetime_start
        self.process_datetime_end = process_datetime_end


class detector_map_qa(Base):
    '''Quality of the detectorMap for the visit
    '''
    __tablename__ = 'detector_map_qa'

    processing_id = Column(Integer,
                           ForeignKey('data_processing_pipe2d.processing_id'),
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True,
                          autoincrement=False
                          )
    camera_name = Column(String(2),
                         primary_key=True,
                         autoincrement=False
                         )
    status_type = Column(String,
                         primary_key=True,
                         autoincrement=False
                         )
    description = Column(String,
                         primary_key=True,
                         autoincrement=False
                         )
    spectrograph = Column(Integer,
                          comment='')
    arm = Column(String(1),
                 comment='')
    observation_reason = Column(String,
                                comment='')
    dof = Column(REAL,
                 comment='')
    chi2x = Column(REAL,
                   comment='')
    chi2y = Column(REAL,
                   comment='')
    spatial_median = Column(REAL,
                            comment='')
    spatial_robust_rms = Column(REAL,
                                comment='')
    spatial_weighted_rms = Column(REAL,
                                  comment='')
    spatial_soften_fit = Column(REAL,
                                comment='')
    spatial_dof = Column(REAL,
                         comment='')
    spatial_num_fibers = Column(Integer,
                                comment='')
    spatial_num_lines = Column(Integer,
                               comment='')
    wavelength_median = Column(REAL,
                               comment='')
    wavelength_robust_rms = Column(REAL,
                                   comment='')
    wavelength_weighted_rms = Column(REAL,
                                     comment='')
    wavelength_soften_fit = Column(REAL,
                                   comment='')
    wavelength_dof = Column(REAL,
                            comment='')
    wavelength_num_fibers = Column(Integer,
                                   comment='')
    wavelength_num_lines = Column(Integer,
                                  comment='')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 camera_name,
                 status_type,
                 description,
                 spectrograph,
                 arm,
                 observation_reason,
                 dof,
                 chi2x,
                 chi2y,
                 spatial_median,
                 spatial_robust_rms,
                 spatial_weighted_rms,
                 spatial_soften_fit,
                 spatial_dof,
                 spatial_num_fibers,
                 spatial_num_lines,
                 wavelength_median,
                 wavelength_robust_rms,
                 wavelength_weighted_rms,
                 wavelength_soften_fit,
                 wavelength_dof,
                 wavelength_num_fibers,
                 wavelength_num_lines,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.camera_name = camera_name
        self.status_type = status_type
        self.description = description
        self.spectrograph = spectrograph
        self.arm = arm
        self.observation_reason = observation_reason
        self.dof = dof
        self.chi2x = chi2x
        self.chi2y = chi2y
        self.spatial_median = spatial_median
        self.spatial_robust_rms = spatial_robust_rms
        self.spatial_weighted_rms = spatial_weighted_rms
        self.spatial_soften_fit = spatial_soften_fit
        self.spatial_dof = spatial_dof
        self.spatial_num_fibers = spatial_num_fibers
        self.spatial_num_lines = spatial_num_lines
        self.wavelength_median = wavelength_median
        self.wavelength_robust_rms = wavelength_robust_rms
        self.wavelength_weighted_rms = wavelength_weighted_rms
        self.wavelength_soften_fit = wavelength_soften_fit
        self.wavelength_dof = wavelength_dof
        self.wavelength_num_fibers = wavelength_num_fibers
        self.wavelength_num_lines = wavelength_num_lines


class extraction_qa(Base):
    '''Quality of the extraction for the visit
    '''
    __tablename__ = 'extraction_qa'

    processing_id = Column(Integer,
                           ForeignKey('data_processing_pipe2d.processing_id'),
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True,
                          autoincrement=False
                          )
    camera_name = Column(String(2),
                         primary_key=True,
                         autoincrement=False
                         )
    fiber_id = Column(Integer,
                      primary_key=True,
                      autoincrement=False
                      )
    spectrograph = Column(Integer,
                          comment='')
    arm = Column(String(1),
                 comment='')
    xa = Column(REAL,
                comment='')
    pfs_arm_ave = Column(REAL,
                         comment='')
    chi2 = Column(REAL,
                  comment='')
    chi_ave = Column(REAL,
                     comment='')
    chi_med = Column(REAL,
                     comment='')
    chi_std = Column(REAL,
                     comment='')
    chi_at_peak = Column(REAL,
                         comment='')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 camera_name,
                 fiber_id,
                 spectrograph,
                 arm,
                 xa,
                 pfs_arm_ave,
                 chi2,
                 chi_ave,
                 chi_med,
                 chi_std,
                 chi_at_peak,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.camera_name = camera_name
        self.fiber_id = fiber_id
        self.spectrograph = spectrograph
        self.arm = arm
        self.xa = xa
        self.pfs_arm_ave = pfs_arm_ave
        self.chi2 = chi2
        self.chi_ave = chi_ave
        self.chi_med = chi_med
        self.chi_std = chi_std
        self.chi_at_peak = chi_at_peak


class sky_subtraction_qa_sa(Base):
    '''Summary of the quality of the sky subtraction for each visit (QA to detect significant over/under subtraction)
    '''
    __tablename__ = 'sky_subtraction_qa_sa'

    processing_id = Column(Integer,
                           ForeignKey('data_processing_pipe2d.processing_id'),
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True,
                          autoincrement=False
                          )
    number_of_sky_fibers = Column(Integer,
                                  comment='the number of sky fibers to make the sky model')
    skysub_median_avg = Column(REAL,
                               comment='TBW')
    skysub_median_under = Column(REAL,
                                 comment='TBW')
    skysub_median_over = Column(REAL,
                                comment='TBW')
    skysub_median_abs = Column(REAL,
                               comment='TBW')
    skysub_continuum_flux_fit_median = Column(REAL,
                                              comment='the median of residual of sky-subtracted sky spectra (electrons/nm)')
    skysub_continuum_sky_fit_median = Column(REAL,
                                             comment='the median of sky spectra (electrons/nm)')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 number_of_sky_fibers,
                 skysub_median_avg,
                 skysub_median_under,
                 skysub_median_over,
                 skysub_median_abs,
                 skysub_continuum_flux_fit_median,
                 skysub_continuum_sky_fit_median,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.number_of_sky_fibers = number_of_sky_fibers
        self.skysub_median_avg = skysub_median_avg
        self.skysub_median_under = skysub_median_under
        self.skysub_median_over = skysub_median_over
        self.skysub_median_abs = skysub_median_abs
        self.skysub_continuum_flux_fit_median = skysub_continuum_flux_fit_median
        self.skysub_continuum_sky_fit_median = skysub_continuum_sky_fit_median


class sky_subtraction_qa_sa_continuum(Base):
    '''Quality of the sky subtraction (continuum) for each visit and fiberId (QA to detect significant over/under subtraction)
    '''
    __tablename__ = 'sky_subtraction_qa_sa_continuum'
    __table_args__ = (ForeignKeyConstraint(['processing_id', 'pfs_visit_id'], [
                                           'sky_subtraction_qa_sa.processing_id', 'sky_subtraction_qa_sa.pfs_visit_id']),
                      {})

    processing_id = Column(Integer,
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          primary_key=True,
                          autoincrement=False
                          )
    fiber_id = Column(Integer,
                      primary_key=True,
                      autoincrement=False
                      )
    continuum_residual_fit = Column(REAL,
                                    comment='the median of residual of sky-subtracted sky spectra (electrons/nm)')
    continuum_sky_fit = Column(REAL,
                               comment='the median of sky spectra (electrons/nm)')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 fiber_id,
                 continuum_residual_fit,
                 continuum_sky_fit,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.fiber_id = fiber_id
        self.continuum_residual_fit = continuum_residual_fit
        self.continuum_sky_fit = continuum_sky_fit


class sky_subtraction_qa_sa_line(Base):
    '''Quality of the sky subtraction (lines) for each visit and fiberId (QA to detect significant over/under subtraction)
    '''
    __tablename__ = 'sky_subtraction_qa_sa_line'
    __table_args__ = (ForeignKeyConstraint(['processing_id', 'pfs_visit_id'], [
                                           'sky_subtraction_qa_sa.processing_id', 'sky_subtraction_qa_sa.pfs_visit_id']),
                      {})

    processing_id = Column(Integer,
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          primary_key=True,
                          autoincrement=False
                          )
    fiber_id = Column(Integer,
                      primary_key=True,
                      autoincrement=False
                      )
    subtype = Column(String,
                     primary_key=True,
                     autoincrement=False,
                     comment='subtype of evaluation (avg/under/over/abs)')
    flux_to_sky = Column(REAL,
                         comment='the ratio between residual and sky flux (percent)')
    sky_lines_num = Column(Integer,
                           comment='the number of sky lines used')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 fiber_id,
                 subtype,
                 flux_to_sky,
                 sky_lines_num,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.fiber_id = fiber_id
        self.subtype = subtype
        self.flux_to_sky = flux_to_sky
        self.sky_lines_num = sky_lines_num


class flux_cal_qa(Base):
    '''Quality of the flux calibration for the visit
    '''
    __tablename__ = 'flux_cal_qa'

    processing_id = Column(Integer, ForeignKey('data_processing_pipe2d.processing_id'),
                           primary_key=True,
                           autoincrement=False
                           )
    pfs_visit_id = Column(Integer,
                          ForeignKey('pfs_visit.pfs_visit_id'),
                          primary_key=True,
                          autoincrement=False
                          )
    number_of_flux_standards = Column(Integer,
                                      comment='the number of flux standard stars to calculate the vector')
    merged_filter = Column(REAL,
                           comment='TBD')
    merged_median = Column(REAL,
                           comment='TBD')
    merged_sigma = Column(REAL,
                          comment='TBD')
    merged_sn_median = Column(REAL,
                              comment='TBD')
    merged_sn_sigma = Column(REAL,
                             comment='TBD')
    imag_median = Column(REAL,
                         comment='TBD')
    imag_sigma = Column(REAL,
                        comment='TBD')
    merged_color_filters = Column(REAL,
                                  comment='TBD')
    merged_color_median = Column(REAL,
                                 comment='TBD')
    merged_color_sigma = Column(REAL,
                                comment='TBD')
    single_median = Column(REAL,
                           comment='TBD')
    single_sigma = Column(REAL,
                          comment='TBD')
    single_color_median = Column(REAL,
                                 comment='TBD')
    single_color_sigma = Column(REAL,
                                comment='TBD')
    stellar_sequence_sigma_gri = Column(REAL,
                                        comment='TBD')
    stellar_sequence_sigma_riz = Column(REAL,
                                        comment='TBD')
    stellar_sequence_sigma_izy = Column(REAL,
                                        comment='TBD')

    def __init__(self,
                 processing_id,
                 pfs_visit_id,
                 number_of_flux_standards,
                 merged_filter,
                 merged_median,
                 merged_sigma,
                 merged_sn_median,
                 merged_sn_sigma,
                 imag_median,
                 imag_sigma,
                 merged_color_filters,
                 merged_color_median,
                 merged_color_sigma,
                 single_median,
                 single_sigma,
                 single_color_median,
                 single_color_sigma,
                 stellar_sequence_sigma_gri,
                 stellar_sequence_sigma_riz,
                 stellar_sequence_sigma_izy,
                 ):
        self.processing_id = processing_id
        self.pfs_visit_id = pfs_visit_id
        self.number_of_flux_standards = number_of_flux_standards
        self.merged_filter = merged_filter
        self.merged_median = merged_median
        self.merged_sigma = merged_sigma
        self.merged_sn_median = merged_sn_median
        self.merged_sn_sigma = merged_sn_sigma
        self.imag_median = imag_median
        self.imag_sigma = imag_sigma
        self.merged_color_filters = merged_color_filters
        self.merged_color_median = merged_color_median
        self.merged_color_sigma = merged_color_sigma
        self.single_median = single_median
        self.single_sigma = single_sigma
        self.single_color_median = single_color_median
        self.single_color_sigma = single_color_sigma
        self.stellar_sequence_sigma_gri = stellar_sequence_sigma_gri
        self.stellar_sequence_sigma_riz = stellar_sequence_sigma_riz
        self.stellar_sequence_sigma_izy = stellar_sequence_sigma_izy


class cosmic_rays(Base):
    '''Quality of the cosmic rays detection for the visit
    '''
    __tablename__ = 'cosmic_rays'
    __table_args__ = (UniqueConstraint('run_id', 'spectrograph', 'arm'), {})

    run_id = Column(Integer, ForeignKey('data_qa.run_id'),
                    primary_key=True,
                    unique=False,
                    autoincrement=False
                    )
    spectrograph = Column(Integer,
                          primary_key=True,
                          unique=False,
                          autoincrement=False
                          )
    arm = Column(String(1),
                 primary_key=True,
                 unique=False,
                 autoincrement=False
                 )
    tbd = Column(REAL,
                 comment='TBD')

    def __init__(self,
                 run_id,
                 arm,
                 tbd,
                 ):
        self.run_id = run_id
        self.arm = arm
        self.tbd = tbd


class mask(Base):
    '''Information on the bit masks in the reduced products
    '''
    __tablename__ = 'mask'
    __table_args__ = (UniqueConstraint('run_id', 'spectrograph', 'arm'), {})

    run_id = Column(Integer, ForeignKey('data_qa.run_id'),
                    primary_key=True,
                    unique=False,
                    autoincrement=False
                    )
    spectrograph = Column(Integer,
                          primary_key=True,
                          unique=False,
                          autoincrement=False
                          )
    arm = Column(String(1),
                 primary_key=True,
                 unique=False,
                 autoincrement=False
                 )
    number_of_pix_in_each_bit = Column(Integer,
                                       comment='TBD')

    def __init__(self,
                 run_id,
                 arm,
                 number_of_pix_in_each_bit,
                 ):
        self.run_id = run_id
        self.arm = arm
        self.number_of_pix_in_each_bit = number_of_pix_in_each_bit


class h4_persistence(Base):
    '''Quality of the H4RG persistence correction for the visit
    '''
    __tablename__ = 'h4_persistence'
    __table_args__ = (UniqueConstraint('run_id', 'spectrograph'), {})

    run_id = Column(Integer, ForeignKey('data_qa.run_id'),
                    primary_key=True,
                    unique=False,
                    autoincrement=False
                    )
    spectrograph = Column(Integer,
                          primary_key=True,
                          unique=False,
                          autoincrement=False
                          )
    tbd = Column(REAL,
                 comment='TBD')

    def __init__(self,
                 run_id,
                 spectrograph,
                 tbd,
                 ):
        self.run_id = run_id
        self.spectrograph = spectrograph
        self.tbd = tbd


class dichroic_continuity(Base):
    '''Check the dichroic continuity after merging the arms
    '''
    __tablename__ = 'dichroic_continuity'
    __table_args__ = (UniqueConstraint('run_id', 'spectrograph'), {})

    run_id = Column(Integer, ForeignKey('data_qa.run_id'),
                    primary_key=True,
                    unique=False,
                    autoincrement=False
                    )
    spectrograph = Column(Integer,
                          primary_key=True,
                          unique=False,
                          autoincrement=False
                          )
    br_continuity = Column(REAL,
                           comment='TBD')
    rn_continuity = Column(REAL,
                           comment='TBD')

    def __init__(self,
                 run_id,
                 spectrograph,
                 br_continuity,
                 rn_continuity,
                 ):
        self.run_id = run_id
        self.spectrograph = spectrograph
        self.br_continuity = br_continuity
        self.rn_continuity = rn_continuity


''' 1D DRP '''


class redshift_measurement(Base):
    '''Quality of 1D redshift measurements
    '''
    __tablename__ = 'redshift_measurement'

    run_id = Column(Integer, ForeignKey('data_qa.run_id'),
                    primary_key=True,
                    unique=False,
                    autoincrement=False
                    )
    number_of_galaxies = Column(Integer,
                                comment='the number of galaxies classified')
    chisq_mean = Column(REAL,
                        comment='the mean chi^2 in the fitting')
    chisq_median = Column(REAL,
                          comment='the median chi^2 in the fitting')
    chisq_sigma = Column(REAL,
                         comment='the sigma of the chi^2 in the fitting')

    def __init__(self,
                 run_id,
                 number_of_galaxies,
                 chisq_mean,
                 chisq_median,
                 chisq_sigma,
                 ):
        self.run_id = run_id
        self.number_of_galaxies = number_of_galaxies
        self.chisq_mean = chisq_mean
        self.chisq_median = chisq_median
        self.chisq_sigma = chisq_sigma


def make_database(dbinfo):
    '''
    dbinfo is something like this: postgresql://xxxxx:yyyyy@zzz.zzz.zzz.zz/dbname
    '''
    # engine = create_engine('sqlite:///:memory:', echo=True)
    # engine = create_engine('sqlite:///pfs_proto.sqlite', echo=False)
    engine = create_engine(dbinfo)

    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session()


if __name__ == '__main__':
    import sys
    dbinfo = sys.argv[1]
    print(dbinfo)
    make_database(dbinfo)
