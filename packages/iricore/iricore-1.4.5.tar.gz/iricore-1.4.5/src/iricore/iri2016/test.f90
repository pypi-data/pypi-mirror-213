program test
    logical :: jf(50) = .true.
    logical :: jmag
    integer :: gsize = 1000
    real :: glat(1000), glon(1000)
    integer :: iyyyy = 2015
    integer :: mmdd = 101
    real :: dhour = 5.
    real :: heibeg = 150.
    real :: heiend = 500.
    real :: heistp = 10.
    real :: oarr(100)
    real :: iri_res(20, 1000, 1000)
    character(256) :: datadir = "data/data16"
    integer :: jffalse(16)
    jffalse =  (/2, 3, 4, 5, 11, 21, 22, 25, 27, 28, 29, 33, 34, 35, 36, 47/)
    do i = 1, gsize
        glat(i) = 90.0
        glon(i) = 0.0
    end do
    do i = 1, size(jffalse)
        jf(jffalse(i)) = .false.
    end do
    call iricore(jf, jmag, glat, glon, gsize, iyyyy, mmdd, dhour, heibeg, heiend, heistp, oarr, iri_res, datadir)
!    print *, oarr
end program test